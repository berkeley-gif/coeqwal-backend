#!/usr/bin/env python3
"""
Entity-Source Link Generator
Creates source tracking for all entities based on logical data source assignments.
"""

import pandas as pd
import uuid
from pathlib import Path

def clean_column_names(df):
    """Clean column names with encoding issues"""
    df.columns = df.columns.str.replace('+AF8-', '_')
    return df

def generate_entity_source_links():
    """Generate entity-source links for all entity types"""
    
    # Read source lookup
    sources_df = pd.read_csv("../01_infrastructure/source.csv")
    source_map = dict(zip(sources_df['source'], sources_df['id']))
    
    links = []
    
    # 1. RESERVOIR ENTITIES → Multiple Sources
    print("Processing reservoir entities...")
    reservoirs_df = clean_column_names(pd.read_csv("reservoir_entity.csv"))
    
    for _, reservoir in reservoirs_df.iterrows():
        entity_uuid = str(uuid.uuid4())  # Generate UUID for calsim_entity
        
        # Primary source: CalSim report (for basic entity data)
        links.append({
            'entity_id': entity_uuid,
            'source_id': source_map['calsim_report'],
            'is_primary': True,
            'notes': f'Reservoir entity {reservoir["short_code"]} from CalSim documentation',
            'created_by': 1,
            'updated_by': 1
        })
        
        # Secondary source: GIS data (for physical characteristics)
        links.append({
            'entity_id': entity_uuid,
            'source_id': source_map['geopackage'],
            'is_primary': False,
            'notes': f'Physical characteristics and capacity estimates for {reservoir["short_code"]}',
            'created_by': 1,
            'updated_by': 1
        })
        
        # For major reservoirs, add James Gilbert research
        if str(reservoir.get('is_main_reservoir')).lower() == 'true':
            links.append({
                'entity_id': entity_uuid,
                'source_id': source_map['james_gilbert'],
                'is_primary': False,
                'notes': f'Operational analysis for major reservoir {reservoir["short_code"]}',
                'created_by': 1,
                'updated_by': 1
            })
    
    # 2. CHANNEL ENTITIES → GIS Primary Source
    print("Processing channel entities...")
    channels_df = clean_column_names(pd.read_csv("channel_entities.csv"))
    
    for _, channel in channels_df.iterrows():
        entity_uuid = str(uuid.uuid4())
        
        # Primary: GeoPackage (channels are primarily from GIS)
        links.append({
            'entity_id': entity_uuid,
            'source_id': source_map['geopackage'],
            'is_primary': True,
            'notes': f'Channel geometry and attributes for {channel["short_code"]}',
            'created_by': 1,
            'updated_by': 1
        })
        
        # Secondary: CalSim variables (for flow definitions)
        links.append({
            'entity_id': entity_uuid,
            'source_id': source_map['calsim_variables'],
            'is_primary': False,
            'notes': f'Flow variable definitions for channel {channel["short_code"]}',
            'created_by': 1,
            'updated_by': 1
        })
    
    # 3. INFLOW ENTITIES → CalSim Variables Primary
    print("Processing inflow entities...")
    inflows_df = clean_column_names(pd.read_csv("inflow_entities.csv"))
    
    for _, inflow in inflows_df.iterrows():
        entity_uuid = str(uuid.uuid4())
        
        # Primary: CalSim variables (inflows are model inputs)
        links.append({
            'entity_id': entity_uuid,
            'source_id': source_map['calsim_variables'],
            'is_primary': True,
            'notes': f'Inflow definition and node connection for {inflow["short_code"]}',
            'created_by': 1,
            'updated_by': 1
        })
        
        # Secondary: CalSim report (for documentation)
        links.append({
            'entity_id': entity_uuid,
            'source_id': source_map['calsim_report'],
            'is_primary': False,
            'notes': f'Hydrologic documentation for inflow {inflow["short_code"]}',
            'created_by': 1,
            'updated_by': 1
        })
    
    # Save results
    links_df = pd.DataFrame(links)
    links_df.to_csv("entity_source_links.csv", index=False)
    
    print(f"✅ Created {len(links)} entity-source links")
    print("\nSummary:")
    print(f"- Reservoir links: {len([l for l in links if 'Reservoir' in l['notes']])}")
    print(f"- Channel links: {len([l for l in links if 'Channel' in l['notes']])}")
    print(f"- Inflow links: {len([l for l in links if 'Inflow' in l['notes']])}")
    
    return links_df

if __name__ == "__main__":
    print("🚀 Generating entity-source links...")
    print("=" * 50)
    
    generate_entity_source_links()
    
    print("=" * 50)
    print("✅ Entity source tracking complete!")
    print("\nNext steps:")
    print("1. Review entity_source_links.csv")
    print("2. Load into entity_source_link table")
    print("3. Update entity tables with generated UUIDs") 