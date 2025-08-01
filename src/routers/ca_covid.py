from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select, col, func
from typing import List
from src.database import get_session
from src.models.gold_ca_fact_tables import gold_fact_ca_demand, gold_fact_ca_antibody
from src.dependencies.logger_config import get_logger

logger = get_logger("covid_router")

router = APIRouter()


@router.get("/ca/demand/", response_model=List[gold_fact_ca_demand])
async def get_ca_demand_data(
    limit: int = 100, offset: int = 0, session: Session = Depends(get_session)
):
    """Get paginated Canada COVID-19 test kit demand data from gold_fact_ca_demand"""
    try:
        statement = select(gold_fact_ca_demand).offset(offset).limit(limit)
        ca_data = session.exec(statement).all()
        return ca_data
    except Exception as e:
        logger.error(f"Error fetching Canada COVID-19 data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching Canada COVID-19 data: {str(e)}"
        )


@router.get("/ca/antibody/", response_model=List[gold_fact_ca_antibody])
async def get_ca_antibody_data(
    limit: int = 100, offset: int = 0, session: Session = Depends(get_session)
):
    """Get paginated Canada COVID-19 test kit antibody data from gold_fact_ca_antibody"""
    try:
        statement = select(gold_fact_ca_antibody).offset(offset).limit(limit)
        ca_data = session.exec(statement).all()
        return ca_data
    except Exception as e:
        logger.error(f"Error fetching Canada COVID-19 data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching Canada COVID-19 data: {str(e)}"
        )
