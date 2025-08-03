from sqlalchemy import desc
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select, col, func
from typing import List
from src.database import get_session
from src.models.gold_ca_fact_tables import (
    gold_fact_ca_demand,
    gold_fact_ca_antibody,
    on_site_test_usage,
    antibody_by_age_group,
)
from src.dependencies.logger_config import get_logger


logger = get_logger("covid_router")

router = APIRouter()


@router.get("/ca/demand/", response_model=List[gold_fact_ca_demand])
async def get_ca_demand_data(
    limit: int = 100, offset: int = 0, session: Session = Depends(get_session)
):
    """Get paginated Canada COVID-19 test kit demand data from gold_fact_ca_demand table"""
    try:
        statement = select(gold_fact_ca_demand).offset(offset).limit(limit)
        ca_data = session.exec(statement).all()
        return ca_data
    except Exception as e:
        logger.error(f"Error fetching Canada COVID-19 data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching Canada COVID-19 data: {str(e)}"
        )


@router.get("/ca/demand/onsite_test_usage/", response_model=List[on_site_test_usage])
async def get_ca_onsite_usage(
    limit: int = 100, offset: int = 0, session: Session = Depends(get_session)
):
    """Get paginated Canada COVID-19 on-site test kit usage by region and industry"""
    try:
        statement = (
            select(
                gold_fact_ca_demand.GEO,
                gold_fact_ca_demand.NAICS,
                gold_fact_ca_demand.COVID_19_RAPID_TEST_KITS_DEMAND_AND_USAGE,
                func.avg(gold_fact_ca_demand.VALUE).label("AVERAGE_PERCENTAGE"),
            )
            .where(
                gold_fact_ca_demand.COVID_19_RAPID_TEST_KITS_DEMAND_AND_USAGE
                == "Percent of businesses that used COVID-19 rapid test kits to test on-site employees"
            )
            .group_by(
                gold_fact_ca_demand.GEO,
                gold_fact_ca_demand.NAICS,
                gold_fact_ca_demand.COVID_19_RAPID_TEST_KITS_DEMAND_AND_USAGE,
            )
            .order_by(
                func.avg(gold_fact_ca_demand.VALUE)
                .label("AVERAGE_PERCENTAGE")
                .desc()
                .nulls_last(),
                gold_fact_ca_demand.GEO.asc(),
            )
            .offset(offset)
            .limit(limit)
        )

        results = session.exec(statement).all()
        return results
    except Exception as e:
        logger.error(f"Error fetching Canada COVID-19 data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching Canada COVID-19 data: {str(e)}"
        )


@router.get("/ca/antibody/", response_model=List[gold_fact_ca_antibody])
async def get_ca_antibody_data(
    limit: int = 100, offset: int = 0, session: Session = Depends(get_session)
):
    """Get paginated Canada COVID-19 antibody data from gold_fact_ca_antibody table"""
    try:
        statement = select(gold_fact_ca_antibody).offset(offset).limit(limit)
        ca_data = session.exec(statement).all()
        return ca_data
    except Exception as e:
        logger.error(f"Error fetching Canada COVID-19 data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching Canada COVID-19 data: {str(e)}"
        )


@router.get("/ca/antibody/age_group/", response_model=List[antibody_by_age_group])
async def get_ca_antibody_by_age_group(
    limit: int = 100, offset: int = 0, session: Session = Depends(get_session)
):
    """Get paginated Canada COVID-19 antibody data by age group"""
    try:
        statement = (
            select(
                gold_fact_ca_antibody.REF_DATE,
                gold_fact_ca_antibody.AGE_GROUP,
                gold_fact_ca_antibody.MEASURE,
                func.round(func.avg(gold_fact_ca_antibody.VALUE), 2).label(
                    "AVERAGE_PERCENTAGE"
                ),
            )
            .where(
                (gold_fact_ca_antibody.CHARACTERISTICS == "Percent")
                & (gold_fact_ca_antibody.MEASURE == "Antibody seroprevalence - Overall")
            )
            .group_by(
                gold_fact_ca_antibody.REF_DATE,
                gold_fact_ca_antibody.AGE_GROUP,
                gold_fact_ca_antibody.MEASURE,
            )
            .order_by(
                func.round(func.avg(gold_fact_ca_antibody.VALUE), 2)
                .label("AVERAGE_PERCENTAGE")
                .desc()
                .nulls_last()
            )
            .offset(offset)
            .limit(limit)
        )
        results = session.exec(statement).all()
        return results
    except Exception as e:
        logger.error(f"Error fetching Canada COVID-19 data: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching Canada COVID-19 data: {str(e)}"
        )
