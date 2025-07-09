-- ============================================================================
-- ENTITY GEOMETRY INTEGRATION SCRIPT
-- Connects CalSim entities with their spatial geometry using PostGIS
-- ============================================================================

-- Step 1: Enable PostGIS extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Step 2: Create temporary geometry tables (load these with ogr2ogr first)
-- ogr2ogr -f PostgreSQL PG:"host=localhost dbname=coeqwal user=postgres" \
--         -nln temp_reservoir_geometry reservoir_points.gpkg
-- ogr2ogr -f PostgreSQL PG:"host=localhost dbname=coeqwal user=postgres" \
--         -nln temp_channel_geometry channel_lines.gpkg
-- ogr2ogr -f PostgreSQL PG:"host=localhost dbname=coeqwal user=postgres" \
--         -nln temp_inflow_geometry inflow_points.gpkg

-- Step 3: Create calsim_entity records for all entity types
-- ============================================================================
-- RESERVOIRS (Points)
-- ============================================================================
INSERT INTO calsim_entity (
    id,
    short_code,
    name,
    entity_type_id,
    hydrologic_region_id,
    geometry,
    is_active,
    created_at,
    created_by,
    updated_at,
    updated_by
)
SELECT 
    gen_random_uuid(),
    re.short_code,
    re.name,
    re.entity_type_id,
    re.hydrologic_region_id,
    CASE 
        WHEN tg.geom IS NOT NULL THEN ST_Transform(tg.geom, 4326)
        ELSE NULL
    END as geometry,
    true,
    NOW(),
    1,  -- System user
    NOW(),
    1
FROM reservoir_entity re
LEFT JOIN temp_reservoir_geometry tg ON re.short_code = tg.reservoir_id
WHERE NOT EXISTS (
    SELECT 1 FROM calsim_entity ce WHERE ce.short_code = re.short_code
);

-- Link reservoir_entity to calsim_entity
UPDATE reservoir_entity re
SET entity_id = ce.id
FROM calsim_entity ce
WHERE re.short_code = ce.short_code
AND re.entity_id IS NULL;

-- ============================================================================
-- CHANNELS (LineStrings)
-- ============================================================================
INSERT INTO calsim_entity (
    id,
    short_code,
    name,
    entity_type_id,
    hydrologic_region_id,
    geometry,
    is_active,
    created_at,
    created_by,
    updated_at,
    updated_by
)
SELECT 
    gen_random_uuid(),
    che.short_code,
    che.name,
    (SELECT id FROM calsim_entity_type WHERE type = 'channel'),
    che.hydrologic_region_id,
    CASE 
        WHEN tcg.geom IS NOT NULL THEN ST_Transform(tcg.geom, 4326)
        ELSE NULL
    END as geometry,
    true,
    NOW(),
    1,
    NOW(),
    1
FROM channel_entity che
LEFT JOIN temp_channel_geometry tcg ON che.short_code = tcg.channel_id
WHERE NOT EXISTS (
    SELECT 1 FROM calsim_entity ce WHERE ce.short_code = che.short_code
);

-- Link channel_entity to calsim_entity
UPDATE channel_entity che
SET entity_id = ce.id
FROM calsim_entity ce
WHERE che.short_code = ce.short_code
AND che.entity_id IS NULL;

-- ============================================================================
-- INFLOWS (Points)
-- ============================================================================
INSERT INTO calsim_entity (
    id,
    short_code,
    name,
    entity_type_id,
    hydrologic_region_id,
    geometry,
    is_active,
    created_at,
    created_by,
    updated_at,
    updated_by
)
SELECT 
    gen_random_uuid(),
    ie.short_code,
    ie.name,
    (SELECT id FROM calsim_entity_type WHERE type = 'inflow'),
    ie.hydrologic_region_id,
    CASE 
        WHEN tig.geom IS NOT NULL THEN ST_Transform(tig.geom, 4326)
        ELSE NULL
    END as geometry,
    true,
    NOW(),
    1,
    NOW(),
    1
FROM inflow_entity ie
LEFT JOIN temp_inflow_geometry tig ON ie.short_code = tig.inflow_id
WHERE NOT EXISTS (
    SELECT 1 FROM calsim_entity ce WHERE ce.short_code = ie.short_code
);

-- Link inflow_entity to calsim_entity
UPDATE inflow_entity ie
SET entity_id = ce.id
FROM calsim_entity ce
WHERE ie.short_code = ce.short_code
AND ie.entity_id IS NULL;

-- Step 4: Create spatial indexes for performance
CREATE INDEX IF NOT EXISTS idx_calsim_entity_geometry 
ON calsim_entity USING GIST (geometry);

CREATE INDEX IF NOT EXISTS idx_calsim_entity_geom_type 
ON calsim_entity (ST_GeometryType(geometry));

CREATE INDEX IF NOT EXISTS idx_calsim_entity_bbox 
ON calsim_entity USING GIST (ST_Envelope(geometry));

-- Step 5: Validation queries
-- ============================================================================
-- Check geometry loading success
SELECT 
    cet.type as entity_type,
    COUNT(*) as total_entities,
    COUNT(ce.geometry) as with_geometry,
    COUNT(*) - COUNT(ce.geometry) as missing_geometry,
    ROUND(100.0 * COUNT(ce.geometry) / COUNT(*), 2) as geometry_coverage_pct
FROM calsim_entity ce
JOIN calsim_entity_type cet ON ce.entity_type_id = cet.id
GROUP BY cet.type
ORDER BY entity_type;

-- Check geometry types
SELECT 
    cet.type as entity_type,
    ST_GeometryType(ce.geometry) as geometry_type,
    COUNT(*) as count
FROM calsim_entity ce
JOIN calsim_entity_type cet ON ce.entity_type_id = cet.id
WHERE ce.geometry IS NOT NULL
GROUP BY cet.type, ST_GeometryType(ce.geometry)
ORDER BY entity_type, geometry_type;

-- Check spatial reference systems
SELECT 
    ST_SRID(geometry) as srid,
    COUNT(*) as count
FROM calsim_entity
WHERE geometry IS NOT NULL
GROUP BY ST_SRID(geometry)
ORDER BY count DESC;

-- Step 6: Sample spatial queries
-- ============================================================================
-- Find entities within 10km of each other
CREATE OR REPLACE VIEW entity_proximity AS
SELECT 
    e1.short_code as entity1,
    e2.short_code as entity2,
    et1.type as entity1_type,
    et2.type as entity2_type,
    ST_Distance(e1.geometry, e2.geometry) / 1000 as distance_km
FROM calsim_entity e1
JOIN calsim_entity e2 ON e1.id < e2.id  -- Avoid duplicates
JOIN calsim_entity_type et1 ON e1.entity_type_id = et1.id
JOIN calsim_entity_type et2 ON e2.entity_type_id = et2.id
WHERE e1.geometry IS NOT NULL 
AND e2.geometry IS NOT NULL
AND ST_DWithin(e1.geometry, e2.geometry, 10000)  -- 10km
ORDER BY distance_km;

-- Channel flow network analysis
CREATE OR REPLACE VIEW channel_network_topology AS
SELECT 
    c1.short_code as upstream_channel,
    c2.short_code as downstream_channel,
    c1.from_node,
    c1.to_node,
    c2.from_node as downstream_from,
    ST_Distance(ce1.geometry, ce2.geometry) as distance_meters
FROM channel_entity c1
JOIN channel_entity c2 ON c1.to_node = c2.from_node
JOIN calsim_entity ce1 ON c1.entity_id = ce1.id
JOIN calsim_entity ce2 ON c2.entity_id = ce2.id
WHERE ce1.geometry IS NOT NULL 
AND ce2.geometry IS NOT NULL
ORDER BY distance_meters;

-- Step 7: Clean up temporary tables
-- DROP TABLE IF EXISTS temp_reservoir_geometry;
-- DROP TABLE IF EXISTS temp_channel_geometry;
-- DROP TABLE IF EXISTS temp_inflow_geometry;

-- ============================================================================
-- USAGE EXAMPLES
-- ============================================================================
/*
-- Find all reservoirs within 50km of Sacramento
SELECT 
    re.short_code,
    re.name,
    ST_Distance(ce.geometry, ST_Point(-121.4944, 38.5816)) / 1000 as distance_km
FROM reservoir_entity re
JOIN calsim_entity ce ON re.entity_id = ce.id
WHERE ST_DWithin(ce.geometry, ST_Point(-121.4944, 38.5816), 50000)
ORDER BY distance_km;

-- Find upstream channels feeding into reservoirs
SELECT 
    che.short_code as channel,
    che.name as channel_name,
    re.short_code as reservoir,
    re.name as reservoir_name,
    ST_Distance(ce1.geometry, ce2.geometry) as distance_meters
FROM channel_entity che
JOIN calsim_entity ce1 ON che.entity_id = ce1.id
JOIN reservoir_entity re ON che.to_node = re.short_code
JOIN calsim_entity ce2 ON re.entity_id = ce2.id
WHERE ce1.geometry IS NOT NULL 
AND ce2.geometry IS NOT NULL
ORDER BY distance_meters;

-- Flow analysis with spatial context
SELECT 
    cv.calsim_id,
    cv.variable_purpose,
    che.short_code as channel,
    ST_Length(ce.geometry) / 1000 as channel_length_km,
    che.hydrologic_region
FROM channel_variable cv
JOIN channel_entity che ON cv.channel_entity_id = che.id
JOIN calsim_entity ce ON che.entity_id = ce.id
WHERE cv.variable_purpose = 'scenario_flow'
AND ce.geometry IS NOT NULL
ORDER BY channel_length_km DESC;
*/ 