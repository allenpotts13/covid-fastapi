from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select, col, func
from typing import List
from src.database import get_session
from src.models.gold_fact_covid_deaths import gold_fact_covid_deaths
from src.dependencies.logger_config import get_logger

logger = get_logger("covid_router")

router = APIRouter()


@router.get("/US/", response_model=List[gold_fact_covid_deaths])
async def get_us_data(
    limit: int = 100, offset: int = 0, session: Session = Depends(get_session)
):
    """Get paginated US COVID-19 data from gold_fact_covid_deaths"""
    try:
        statement = select(gold_fact_covid_deaths).offset(offset).limit(limit)
        us_data = session.exec(statement).all()
        return us_data
    except Exception as e:
        logger.error(f"Error fetching US COVID-19 data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching US COVID-19 data: {str(e)}"
        )


# Return all records matching jurisdiction and month, with pagination
@router.get("/US/aggregate/", response_model=List[gold_fact_covid_deaths])
async def get_by_jurisdiction_and_month(
    jurisdiction_residence_name: str,
    month_name: str,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    """Return all records matching jurisdiction and month, paginated."""
    try:
        logger.info(
            f"/US/aggregate/ params: jurisdiction_residence_name='{jurisdiction_residence_name}', month_name='{month_name}', limit={limit}, offset={offset}"
        )
        stmt = (
            select(gold_fact_covid_deaths)
            .where(
                (
                    gold_fact_covid_deaths.JURISDICTION_RESIDENCE_NAME
                    == jurisdiction_residence_name
                )
                & (gold_fact_covid_deaths.MONTH_NAME == month_name)
            )
            .offset(offset)
            .limit(limit)
        )
        results = session.exec(stmt).all()
        logger.info(f"/US/aggregate/ results_count={len(results)}")
        return results
    except Exception as e:
        logger.error(f"/US/aggregate/ error: {type(e).__name__}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error fetching COVID-19 data: {str(e)}"
        )


@router.get(
    "/US/{jurisdiction_residence_name}", response_model=List[gold_fact_covid_deaths]
)
async def get_us_by_jurisdiction(
    jurisdiction_residence_name: str,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    """Get all US COVID-19 data by jurisdiction residence name, paginated"""
    try:
        # Get all records matching the jurisdiction name, with pagination
        statement = (
            select(gold_fact_covid_deaths)
            .where(
                gold_fact_covid_deaths.JURISDICTION_RESIDENCE_NAME
                == jurisdiction_residence_name
            )
            .offset(offset)
            .limit(limit)
        )
        us_data = session.exec(statement).all()
        if not us_data:
            logger.info(
                f"No data found for jurisdiction name: {jurisdiction_residence_name}"
            )
            raise HTTPException(
                status_code=404, detail="No data found for jurisdiction name"
            )
        return us_data
    except Exception as e:
        logger.error(f"Error fetching US COVID-19 data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching US COVID-19 data: {str(e)}"
        )


@router.get("/US/{month_name}/", response_model=List[gold_fact_covid_deaths])
async def get_us_data_by_month(
    month_name: str,
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    """Get paginated US COVID-19 data for a specific month"""
    try:
        statement = (
            select(gold_fact_covid_deaths)
            .where(gold_fact_covid_deaths.MONTH_NAME == month_name)
            .offset(offset)
            .limit(limit)
        )
        us_data = session.exec(statement).all()
        return us_data
    except Exception as e:
        logger.error(f"Error fetching US COVID-19 data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching US COVID-19 data: {str(e)}"
        )


@router.delete("/US/key/{covid_deaths_key}", status_code=204)
async def delete_us_record(
    covid_deaths_key: int, session: Session = Depends(get_session)
):
    """Delete a US COVID-19 record by COVID_DEATHS_KEY"""
    try:
        record = session.get(gold_fact_covid_deaths, covid_deaths_key)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        session.delete(record)
        session.commit()
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting record: {str(e)}")


@router.put("/US/key/{covid_deaths_key}", response_model=gold_fact_covid_deaths)
async def update_us_record(
    covid_deaths_key: int,
    updated: gold_fact_covid_deaths = Body(...),
    session: Session = Depends(get_session),
):
    """Update a US COVID-19 record by COVID_DEATHS_KEY"""
    try:
        db_record = session.get(gold_fact_covid_deaths, covid_deaths_key)
        if not db_record:
            raise HTTPException(status_code=404, detail="Record not found")
        update_data = updated.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_record, key, value)
        session.add(db_record)
        session.commit()
        session.refresh(db_record)
        return db_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating record: {str(e)}")
