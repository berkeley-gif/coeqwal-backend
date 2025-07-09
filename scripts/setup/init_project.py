#!/usr/bin/env python3
"""
Project initialization script for COEQWAL backend

This script sets up the development environment, initializes the database,
and loads seed data.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def setup_logging():
    """Configure logging for the setup process"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def check_prerequisites() -> bool:
    """Check if required software is installed"""
    logger = logging.getLogger(__name__)
    
    prerequisites = [
        ("python", "Python 3.9+"),
        ("psql", "PostgreSQL client"),
        ("docker", "Docker (optional, for DSS processing)"),
    ]
    
    missing = []
    for cmd, description in prerequisites:
        try:
            subprocess.run([cmd, "--version"], 
                          capture_output=True, check=True)
            logger.info(f"✓ {description} found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(description)
            logger.warning(f"✗ {description} not found")
    
    if missing:
        logger.error(f"Missing prerequisites: {', '.join(missing)}")
        return False
    
    return True

def create_virtual_environment():
    """Create and activate virtual environment"""
    logger = logging.getLogger(__name__)
    
    venv_path = project_root / "venv"
    if venv_path.exists():
        logger.info("Virtual environment already exists")
        return
    
    logger.info("Creating virtual environment...")
    subprocess.run([
        sys.executable, "-m", "venv", str(venv_path)
    ], check=True)
    
    logger.info("Virtual environment created")

def install_dependencies():
    """Install Python dependencies"""
    logger = logging.getLogger(__name__)
    
    venv_python = project_root / "venv" / "bin" / "python"
    if sys.platform == "win32":
        venv_python = project_root / "venv" / "Scripts" / "python.exe"
    
    requirements_file = project_root / "requirements.txt"
    
    logger.info("Installing dependencies...")
    subprocess.run([
        str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)
    ], check=True)
    
    logger.info("Dependencies installed")

def setup_environment_file():
    """Create .env file from template"""
    logger = logging.getLogger(__name__)
    
    env_file = project_root / ".env"
    env_template = project_root / ".env.example"
    
    if env_file.exists():
        logger.info(".env file already exists")
        return
    
    # Create basic .env file
    env_content = """# CalSim Backend Environment Variables
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/calsim_dev

# AWS (for development)
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# Cognito
COGNITO_USER_POOL_ID=your_pool_id_here
COGNITO_CLIENT_ID=your_client_id_here
COGNITO_CLIENT_SECRET=your_client_secret_here

# Security
SECRET_KEY=dev-secret-key-change-in-production

# Redis
REDIS_URL=redis://localhost:6379/0
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    logger.info(".env file created")

def init_database():
    """Initialize the database"""
    logger = logging.getLogger(__name__)
    
    # Check if database exists
    try:
        from config.environments.development import DevelopmentConfig
        db_url = DevelopmentConfig.get_database_url()
        
        logger.info("Database configuration loaded")
        logger.info("To initialize the database, run:")
        logger.info("  python scripts/setup/create_database.py")
        logger.info("  python scripts/setup/run_migrations.py")
        logger.info("  python database/seed_tables/load_seeds.py")
        
    except Exception as e:
        logger.warning(f"Database setup will need to be done manually: {e}")

def create_data_directories():
    """Create data storage directories"""
    logger = logging.getLogger(__name__)
    
    data_dirs = [
        "data/raw/dss_files",
        "data/raw/gis_data", 
        "data/processed/csv_files",
        "data/exports/reports",
        "logs"
    ]
    
    for dir_path in data_dirs:
        full_path = project_root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")

def main():
    """Main setup process"""
    logger = setup_logging()
    logger.info("🚀 Initializing CalSim Backend project...")
    
    # Check prerequisites
    if not check_prerequisites():
        logger.error("Prerequisites check failed. Please install missing software.")
        sys.exit(1)
    
    # Setup steps
    try:
        create_virtual_environment()
        install_dependencies()
        setup_environment_file()
        create_data_directories()
        init_database()
        
        logger.info("🎉 Project initialization complete!")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Activate virtual environment: source venv/bin/activate")
        logger.info("2. Update .env file with your AWS credentials")
        logger.info("3. Set up PostgreSQL database")
        logger.info("4. Run database migrations")
        logger.info("5. Load seed data")
        logger.info("6. Start development server: python api/app.py")
        
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 