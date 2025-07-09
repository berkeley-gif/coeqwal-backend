# COEQWAL Backend

A comprehensive backend system for COEQWAL data, themes, scenarios, and analytics.

## 🏗️ Repository Structure

```
coeqwal-backend/
├── 📊 database/              # Database schema, migrations, and seed data
│   ├── migrations/           # Database migration files
│   ├── schema/              # ERD and table definitions
│   ├── seed_tables/         # Initial data for lookup tables  
│   └── fixtures/            # Test data and sample datasets
├── 🔄 etl/                  # Extract, Transform, Load processes
│   ├── pipelines/           # ETL workflow definitions
│   ├── transformers/        # Data transformation logic
│   ├── loaders/             # Database loading utilities
│   └── validators/          # Data quality and validation
├── 🌐 api/                  # REST API and web services
│   ├── routes/              # API endpoint definitions
│   ├── models/              # Data models and ORM
│   ├── middleware/          # Authentication, CORS, etc.
│   └── services/            # Business logic services
├── ☁️ infrastructure/        # AWS and deployment configuration
│   ├── aws/                 # AWS service configurations
│   ├── terraform/           # Infrastructure as Code
│   └── docker/              # Container definitions
├── ⚙️ config/               # Application configuration
│   ├── environments/        # Environment-specific settings
│   └── secrets/            # Secret management (encrypted)
├── 📁 data/                 # Data storage and processing
│   ├── raw/                # Raw input data files
│   ├── processed/          # Cleaned and transformed data
│   ├── exports/            # Generated outputs and reports
│   └── lookups/            # Reference data and mappings
├── 📚 docs/                 # Documentation
│   ├── api/                # API documentation
│   ├── database/           # Database documentation
│   ├── etl/                # ETL process documentation
│   └── deployment/         # Deployment guides
├── 🛠️ scripts/              # Utility scripts
│   ├── setup/              # Environment setup scripts
│   ├── maintenance/        # Database maintenance
│   └── utilities/          # General utilities
└── 📈 monitoring/           # Observability and monitoring
    ├── logs/               # Log configurations
    ├── metrics/            # Metrics and dashboards
    └── alerts/             # Alert configurations
```

## 🚀 Quick start

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- AWS CLI configured
- Docker (optional)

### Setup
```bash
# Clone and setup
git clone <repository-url>
cd coeqwal-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Initialize database
python scripts/setup/init_database.py

# Load seed data
python scripts/setup/load_seed_data.py

# Run tests
pytest tests/

# Start development server
python api/app.py
```

## 📊 Database

### Schema management
- **ERD**: Located in `database/schema/erd.txt`
- **Migrations**: Versioned schema changes in `database/migrations/`
- **Seeds**: Lookup table data in `database/seed_tables/`

## 🔄 ETL processes

### Data Pipeline
1. **Extract**: Raw CalSim data, GIS data, research inputs
2. **Transform**: Data cleaning, validation, normalization, calculations
3. **Load**: Database insertion with proper relationships

### Key Pipelines
- **DSS processing**: Integration with existing DSS tools
- **GIS integration**: Spatial data processing
- **Variable mapping**: CalSim variable normalization
- **Calculate outcome statistics**
- **Calculate tiers**

## 🌐 API

### Endpoints
- `/api/v1/themes/` - Theme management
- `/api/v1/scenarios/` - Scenario operations
- `/api/v1/variables/` - CalSim variable data
- `/api/v1/statistics/` - Summary statistics

## ☁️ Infrastructure

### AWS Services
- **RDS PostgreSQL**: Primary database
- **S3**: Data storage and backups
- **Lambda**: ETL processing
- **API Gateway**: API hosting

### Deployment
- Terraform for infrastructure provisioning
- Docker containers for consistent environments

## 📈 Monitoring

### Observability
- CloudWatch logs and metrics
- Database performance monitoring
- ETL pipeline monitoring
- API response time tracking