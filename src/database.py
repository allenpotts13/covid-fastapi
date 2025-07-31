import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from typing import Generator, Optional

# Load environment variables from .env file
load_dotenv()

# Snowflake connection parameters
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD") 
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")

# Global variables for engine and session
engine: Optional[object] = None
SessionLocal: Optional[object] = None

def init_database():
    """Initialize database connection with environment variables"""
    global engine, SessionLocal
    
    # Check if all required environment variables are present
    required_vars = [
        SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT,
        SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA, SNOWFLAKE_WAREHOUSE
    ]
    
    if not all(required_vars):
        missing_vars = []
        if not SNOWFLAKE_USER: missing_vars.append("SNOWFLAKE_USER")
        if not SNOWFLAKE_PASSWORD: missing_vars.append("SNOWFLAKE_PASSWORD")
        if not SNOWFLAKE_ACCOUNT: missing_vars.append("SNOWFLAKE_ACCOUNT")
        if not SNOWFLAKE_DATABASE: missing_vars.append("SNOWFLAKE_DATABASE")
        if not SNOWFLAKE_SCHEMA: missing_vars.append("SNOWFLAKE_SCHEMA")
        if not SNOWFLAKE_WAREHOUSE: missing_vars.append("SNOWFLAKE_WAREHOUSE")
        
        print(f"Warning: Missing Snowflake environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with your Snowflake credentials")
        return False
    
    try:
        # Create Snowflake connection string
        CONNECTION_STRING = (
            f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/"
            f"{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}?warehouse={SNOWFLAKE_WAREHOUSE}"
        )
        
        if SNOWFLAKE_ROLE:
            CONNECTION_STRING += f"&role={SNOWFLAKE_ROLE}"
        
        # Create engine
        engine = create_engine(
            CONNECTION_STRING,
            echo=False,  # Set to True for debugging
            pool_pre_ping=True
        )
        
        # Session will be created directly using SQLModel.Session
        SessionLocal = engine
        print("Database connection initialized successfully")
        return True
        
    except Exception as e:
        print(f"Failed to initialize database: {str(e)}")
        return False

def create_db_and_tables():
    """Create database tables"""
    if engine is None:
        print("Database not initialized. Skipping table creation.")
        return
    
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Failed to create tables: {str(e)}")

def get_session() -> Generator:
    """Get database session"""
    if SessionLocal is None:
        raise Exception("Database not initialized. Please set up your .env file with Snowflake credentials.")
    
    with Session(SessionLocal) as session:
        yield session
