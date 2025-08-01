from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Date

class gold_fact_ukhsa_vaccinations(SQLModel, table=True):
    __tablename__ = "gold_fact_ukhsa_vaccinations"

    ID: Optional[int] = Field(default=None, primary_key=True, description="Unique key for vax records across area, age bands, and dose type")
    DATE: Optional[str] = Field(default=None, description="Day of measurement")
    AGE_CATEGORY: Optional[str] = Field(default=None, description="Category of age range")
    MIN_AGE: Optional[int] = Field(default=None, description="Minimum age of an age category")
    MAX_AGE: Optional[int] = Field(default=None, description="Maximum age of an age category")
    AREA_NAME: Optional[str] = Field(default=None, description="Name of area measured")
    AREA_TYPE: Optional[str] = Field(default=None, description="Type of area measured")
    COUNTRY: Optional[str] = Field(default=None, description="Country of area measured")
    DOSE_LABEL: Optional[str] = Field(default=None, description="Dose type administered")
    DOSE_CATEGORY: Optional[str] = Field(default=None, description="Category of dose administered")
    DOSE_COUNT: Optional[int] = Field(default=None, description="Number of doses administered")