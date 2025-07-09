"""
Development environment configuration
"""
import os
from typing import Optional

class DevelopmentConfig:
    """Development environment settings"""
    
    # Application
    ENV = "development"
    DEBUG = True
    TESTING = False
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password@localhost:5432/calsim_dev"
    )
    DATABASE_ECHO = True  # Log SQL queries in development
    
    # AWS Settings (local development)
    AWS_REGION = "us-west-2"
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # S3
    S3_BUCKET = "calsim-dev-data"
    S3_PREFIX = "development/"
    
    # Cognito (development pool)
    COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
    COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
    COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
    
    # API
    API_HOST = "localhost"
    API_PORT = 8000
    API_WORKERS = 1
    API_RELOAD = True
    
    # ETL Settings
    ETL_BATCH_SIZE = 1000
    ETL_MAX_WORKERS = 4
    ETL_TIMEOUT = 300  # 5 minutes
    
    # DSS Integration
    DSS_DOCKER_IMAGE = "pydsstools:latest"
    DSS_TEMP_DIR = "/tmp/dss_processing"
    DSS_REPO_PATH = "../COEQWAL-pydsstools"  # Path to your existing DSS repo
    
    # Data Directories
    DATA_ROOT = "data/"
    RAW_DATA_DIR = "data/raw/"
    PROCESSED_DATA_DIR = "data/processed/"
    EXPORT_DATA_DIR = "data/exports/"
    
    # Logging
    LOG_LEVEL = "DEBUG"
    LOG_FORMAT = "json"
    LOG_FILE = "logs/calsim-dev.log"
    
    # Redis (for caching)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Feature Flags
    ENABLE_GIS_PROCESSING = True
    ENABLE_REAL_TIME_STATS = False
    ENABLE_ADVANCED_ANALYTICS = True
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24
    
    # CORS (permissive for development)
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8080"]
    CORS_CREDENTIALS = True
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get formatted database URL"""
        return cls.DATABASE_URL
    
    @classmethod
    def get_s3_config(cls) -> dict:
        """Get S3 configuration"""
        return {
            "bucket": cls.S3_BUCKET,
            "prefix": cls.S3_PREFIX,
            "region": cls.AWS_REGION
        }
    
    @classmethod
    def get_etl_config(cls) -> dict:
        """Get ETL configuration"""
        return {
            "batch_size": cls.ETL_BATCH_SIZE,
            "max_workers": cls.ETL_MAX_WORKERS,
            "timeout": cls.ETL_TIMEOUT,
            "dss_image": cls.DSS_DOCKER_IMAGE,
            "temp_dir": cls.DSS_TEMP_DIR,
            "repo_path": cls.DSS_REPO_PATH
        } 