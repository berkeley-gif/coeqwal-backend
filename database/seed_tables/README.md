# Database Seed Data

This directory contains CSV files and scripts to populate lookup tables and initial data.

## 📁 File Organization

```
seed_tables/
├── 00_versioning/          # Versioning system
│   ├── user.csv
│   ├── version.csv
│   ├── version_family.csv
│   └── domain_family_map.csv
├── 01_infrastructure/       # Core system tables
│   ├── hydrologic_region.csv
│   ├── unit.csv
│   ├── source.csv
│   ├── spatial_scale.csv
│   └── temporal_scale.csv
├── 02_entity_system/        # CalSim entity framework
│   ├── calsim_entity_type.csv
│   ├── calsim_schematic_type.csv
│   └── variable_type.csv
├── 03_outcome_framework/    # Outcome and measurement tables
│   ├── outcome_category.csv
│   └── statistic_type.csv
├── 04_calsim_data/         # CalSim entity and variable data
│   ├── reservoir_entity.csv
│   ├── reservoir_variables.csv
│   ├── inflow_entity.csv
│   ├── inflow_variables.csv
│   ├── channel_entities.csv
│   ├── channel_variables.csv
│   ├── entity_source_links.csv
│   └── create_entity_source_links.py
├── 05_themes_scenarios/    # Research themes and scenarios (empty)
├── 06_assumptions_operations/  # Policy assumptions and operational rules
│   ├── assumption_category.csv
│   ├── assumption_definition.csv
│   ├── operation_category.csv
│   ├── operation_definition.csv
│   └── README.md
├── 07_hydroclimate/        # Hydroclimate data
│   └── hydroclimate.csv
└── README.md               # This file
```

## 🔄 Loading Order

Seed data must be loaded in dependency order:

1. **Infrastructure** - Core lookup tables
2. **Entity System** - CalSim framework tables  
3. **Outcome Framework** - Measurement and statistics
4. **CalSim Data** - Your organized channel, inflow, reservoir data
5. **Themes & Scenarios** - Research framework data
6. **Assumptions & Operations** - Policy assumptions and operational rules
7. **Hydroclimate** - Climate and hydrology data

## 🚀 Usage

```bash
# Load all seed data
python database/seed_tables/load_seeds.py

# Load specific category
python database/seed_tables/load_seeds.py --category infrastructure

# Reset and reload
python database/seed_tables/load_seeds.py --reset
```

## 📝 CSV Format

All CSV files should:
- Use UTF-8 encoding
- Include headers in first row
- Use consistent null representation (empty string or NULL)
- Follow naming convention: `table_name.csv`

## 🔗 Relationships

The loading script automatically handles foreign key relationships by loading in the correct order.

## 🎯 Key Files in 04_calsim_data

The CalSim data directory contains the main entity and variable tables:

### **Entity Tables**
- `reservoir_entity.csv` - Reservoir entities with physical characteristics
- `inflow_entity.csv` - Inflow points where water enters the system  
- `channel_entities.csv` - Channel/stream/canal segments

### **Variable Tables**
- `reservoir_variables.csv` - Storage and operational variables
- `inflow_variables.csv` - Inflow rate variables (I_*)
- `channel_variables.csv` - Flow variables (C_*, UI_*, MF_*)

### **Source Tracking**
- `entity_source_links.csv` - Links entities to their data sources
- `create_entity_source_links.py` - Script to generate source links

### **Migration Scripts**
- `migrate_complete_data.py` - Complete data migration script
- `migrate_all_data.py` - Alternative migration approach 