from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select, col, func
from typing import List
from src.database import get_session
from src.models.gold_fact_ukhsa_vaccinations import gold_fact_ukhsa_vaccinations
from src.dependencies.logger_config import get_logger

logger = get_logger("covid_router")

router = APIRouter()

@router.get("/UKHSA/", response_model=List[gold_fact_ukhsa_vaccinations])
async def get_ukhsa_data(
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get paginated UKHSA COVID-19 vaccination data from gold_fact_ukhsa_vaccinations"""
    try:
        statement = select(gold_fact_ukhsa_vaccinations).offset(offset).limit(limit)
        ukhsa_data = session.exec(statement).all()
        return ukhsa_data
    except Exception as e:
        logger.error(f"Error fetching UKHSA COVID-19 vaccination data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching UKHSA COVID-19 vaccination data: {str(e)}")

# Return all records matching jurisdiction and month, with pagination
@router.get("/UKHSA/aggregate/", response_model=List[gold_fact_ukhsa_vaccinations])
async def get_by_area_name_and_date(
    date: str,
    area_name: str,
    age_category: str,
    dose_type: str,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Return all records matching area_name and date, paginated."""
    try:
        logger.info(f"/UKHSA/aggregate/ params: area_name='{area_name}', date='{date}', limit={limit}, offset={offset}")
        stmt = (
            select(gold_fact_ukhsa_vaccinations)
            .where(
                (gold_fact_ukhsa_vaccinations.DATE == date) &
                (gold_fact_ukhsa_vaccinations.AREA_NAME == area_name) &
                (gold_fact_ukhsa_vaccinations.AGE_CATEGORY == age_category) &
                (gold_fact_ukhsa_vaccinations.DOSE_LABEL == dose_type)
            )
            .offset(offset)
            .limit(limit)
        )
        results = session.exec(stmt).all()
        logger.info(f"/UKHSA/aggregate/ results_count={len(results)}")
        return results
    except Exception as e:
        logger.error(f"/UKHSA/aggregate/ error: {type(e).__name__}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching COVID-19 vaccination data: {str(e)}")

@router.get("/UKHSA/area/{area_name}", response_model=List[gold_fact_ukhsa_vaccinations])
async def get_ukhsa_by_area_name(
    area_name: str,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get all US COVID-19 data by area name, paginated"""
    try:
        # Get all records matching the jurisdiction name, with pagination
        statement = select(gold_fact_ukhsa_vaccinations).where(
            gold_fact_ukhsa_vaccinations.AREA_NAME == area_name
        ).offset(offset).limit(limit)
        ukhsa_data = session.exec(statement).all()
        if not ukhsa_data:
            logger.info(f"No data found for area name: {area_name}")
            raise HTTPException(status_code=404, detail="No data found for area name")
        return ukhsa_data
    except Exception as e:
        logger.error(f"Error fetching UKHSA COVID-19 vaccination data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching UKHSA COVID-19 vaccination data: {str(e)}")

@router.get("/UKHSA/date/{date}", response_model=List[gold_fact_ukhsa_vaccinations])
async def get_ukhsa_by_date(
    date: str,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get paginated US COVID-19 data for a specific date"""
    try:
        statement = select(gold_fact_ukhsa_vaccinations).where(
            gold_fact_ukhsa_vaccinations.DATE == date
        ).offset(offset).limit(limit)
        ukhsa_data = session.exec(statement).all()
        return ukhsa_data
    except Exception as e:
        logger.error(f"Error fetching UKHSA COVID-19 vaccination data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching UKHSA COVID-19 vaccination data: {str(e)}")
    
@router.get("/UKHSA/age_category/{age_category}", response_model=List[gold_fact_ukhsa_vaccinations])
async def get_ukhsa_by_age_category(
    age_category: str,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get paginated US COVID-19 data for a specific age category"""
    try:
        statement = select(gold_fact_ukhsa_vaccinations).where(
            gold_fact_ukhsa_vaccinations.AGE_CATEGORY == age_category
        ).offset(offset).limit(limit)
        ukhsa_data = session.exec(statement).all()
        return ukhsa_data
    except Exception as e:
        logger.error(f"Error fetching UKHSA COVID-19 vaccination data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching UKHSA COVID-19 vaccination data: {str(e)}")
    
@router.get("/UKHSA/dose/{dose_type}", response_model=List[gold_fact_ukhsa_vaccinations])
async def get_ukhsa_by_dose_type(
    dose_type: str,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    """Get paginated US COVID-19 data for a specific age category"""
    try:
        statement = select(gold_fact_ukhsa_vaccinations).where(
            gold_fact_ukhsa_vaccinations.DOSE_LABEL == dose_type
        ).offset(offset).limit(limit)
        ukhsa_data = session.exec(statement).all()
        return ukhsa_data
    except Exception as e:
        logger.error(f"Error fetching UKHSA COVID-19 vaccination data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching UKHSA COVID-19 vaccination data: {str(e)}")
    