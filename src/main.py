from fastapi import FastAPI
from src.database import init_database, create_db_and_tables
from src.routers import us_covid, ca_covid, ukhsa_vax

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="COVID Data API", description="API for COVID-19 data", version="1.0.0", docs_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_css_url="/static/custom-swagger.css"
    )

# Include routers
app.include_router(us_covid.router, prefix="/api/v1", tags=["US COVID Data"])
app.include_router(ukhsa_vax.router, prefix="/api/v1", tags=["UKHSA COVID Vax Data"])
app.include_router(ca_covid.router, prefix="/api/v1", tags=["Canada COVID Data"])   


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
        "us_endpoints": {
            "all_covid_data": "/api/v1/US/",
            "covid_by_jurisdiction": "/api/v1/US/{jurisdiction_residence_name}",
            "covid_by_month": "/api/v1/US/{month_name}/",
            "delete_by_key": "/api/v1/US/key/{covid_deaths_key}",
            "update_by_key": "/api/v1/US/key/{covid_deaths_key}",
            "health": "/health",
        },
        "canada_endpoints": {
            "ca_demand_data": "/api/v1/ca/demand/",
            "ca_antibody_data": "/api/v1/ca/antibody/",
        },
        "ukhsa_endpoints": {
            "all_vaccination_data": "/api/v1/UKHSA",
            "vaccinations_by_area": "/api/v1/UKHSA/{area_name}",
            "vaccinations_by_date": "/api/v1/UKHSA/{date}",
            "vaccinations_by_age_category": "/api/v1/UKHSA/{age_category}",
            "health": "/health",
        },
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
