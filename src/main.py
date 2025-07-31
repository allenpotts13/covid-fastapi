from fastapi import FastAPI
from src.database import init_database, create_db_and_tables
from src.routers import covid

app = FastAPI(title="COVID Data API", description="API for COVID-19 data", version="1.0.0")

# Include routers
app.include_router(covid.router, prefix="/api/v1", tags=["US COVID Data"])

@app.on_event("startup")
def on_startup():
    # Initialize database connection first
    db_initialized = init_database()
    if db_initialized:
        create_db_and_tables()

@app.get("/")
async def root():
    return {
        "message": "COVID Data API is running!",
        "docs": "/docs",
        "endpoints": {
            "all_covid_data": "/api/v1/US/",
            "covid_by_jurisdiction": "/api/v1/US/{jurisdiction_residence_name}",
            "covid_by_month": "/api/v1/US/{month_name}/",
            "delete_by_key": "/api/v1/US/key/{covid_deaths_key}",
            "update_by_key": "/api/v1/US/key/{covid_deaths_key}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}