from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, DateTime

class gold_fact_covid_deaths(SQLModel, table=True):
    __tablename__ = "gold_fact_covid_deaths"

    COVID_DEATHS_KEY: Optional[int] = Field(default=None, primary_key=True, description="Unique key for COVID deaths")
    JURISDICTION_RESIDENCE_CODE: Optional[str] = Field(default=None, description="Code for jurisdiction residence")
    JURISDICTION_RESIDENCE_NAME: Optional[str] = Field(default=None, description="Name of the jurisdiction residence")
    MONTH_CODE: Optional[str] = Field(default=None, description="Month code")
    MONTH_NAME: Optional[str] = Field(default=None, description="Month name")
    DEMOGRAPHIC_GROUP_CODE: Optional[str] = Field(default=None, description="Demographic group code")
    DEMOGRAPHIC_GROUP_NAME: Optional[str] = Field(default=None, description="Demographic group name")
    SUBGROUP1_CODE: Optional[str] = Field(default=None, description="Subgroup 1 code")
    SUBGROUP1_NAME: Optional[str] = Field(default=None, description="Subgroup 1 name")
    SUBGROUP2_CODE: Optional[str] = Field(default=None, description="Subgroup 2 code")
    SUBGROUP2_NAME: Optional[str] = Field(default=None, description="Subgroup 2 name")
    YEAR: Optional[int] = Field(default=None, description="Year")
    COVID_DEATHS: Optional[float] = Field(default=None, description="Number of COVID-19 deaths")
    CRUDE_COVID_RATE: Optional[float] = Field(default=None, description="Crude COVID rate")
    AA_COVID_RATE: Optional[float] = Field(default=None, description="Age-adjusted COVID rate")
    CRUDE_COVID_RATE_ANN: Optional[float] = Field(default=None, description="Annualized crude COVID rate")
    AA_COVID_RATE_ANN: Optional[float] = Field(default=None, description="Annualized age-adjusted COVID rate")
    FOOTNOTE: Optional[str] = Field(default=None, description="Footnote")
    IS_SUPPRESSED_DEATH_COUNT: Optional[bool] = Field(default=None, description="Is suppressed death count")
    IS_SUPPRESSION_NOTE: Optional[bool] = Field(default=None, description="Is suppression note")
   