from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, DateTime


class gold_fact_ca_demand(SQLModel, table=True):
    __tablename__ = "FACT_CA_DEMAND"

    ID: Optional[int] = Field(
        default=None, primary_key=True, description="Unique identifier"
    )
    REF_DATE: Optional[str] = Field(
        default=None, description="Reference date (e.g., 2022-01)"
    )
    GEO: Optional[str] = Field(
        default=None, description="Geographic name (e.g., Canada)"
    )
    DGUID: Optional[str] = Field(
        default=None, description="Detailed geographic unique identifier"
    )

    NAICS: Optional[str] = Field(
        default=None,
        sa_column=Column("NORTH_AMERICAN_INDUSTRY_CLASSIFICATION_SYSTEM_(NAICS)"),
        description="Industry name based on North American Industry Classification System (NAICS)",
    )

    COVID_19_RAPID_TEST_KITS_DEMAND_AND_USAGE: Optional[str] = Field(
        default=None,
        alias="COVID_19_RAPID_TEST_KITS_DEMAND_AND_USAGE",
        description="Description of rapid test kit demand and usage",
    )
    UOM_ID: Optional[int] = Field(default=None, description="Unit of measure ID")
    SCALAR_FACTOR: Optional[str] = Field(
        default=None, description="Scalar factor used in value representation"
    )
    SCALAR_ID: Optional[int] = Field(default=None, description="Scalar ID")
    VECTOR: Optional[str] = Field(
        default=None, description="Vector code used for internal metadata"
    )
    COORDINATE: Optional[str] = Field(default=None, description="Coordinate identifier")
    VALUE: Optional[float] = Field(default=None, description="Measured value")
    STATUS: Optional[str] = Field(default=None, description="Status flag")
    STATUS_DESCRIPTION: Optional[str] = Field(
        default=None, description="Description of the status or quality of data"
    )
    DECIMALS: Optional[int] = Field(
        default=None, description="Number of decimal places in the value"
    )
    INGESTION_DATE: Optional[datetime] = Field(
        default=None, description="Date and time the data was ingested"
    )
    FILENAME: Optional[str] = Field(default=None, description="Source CSV filename")


class gold_fact_ca_antibody(SQLModel, table=True):
    __tablename__ = "FACT_CA_ANTIBODY"

    ID: Optional[int] = Field(
        default=None, primary_key=True, description="Unique identifier for the record"
    )
    REF_DATE: Optional[int] = Field(
        default=None, description="Reference date as numeric code (e.g., YYYYMM)"
    )
    GEO: Optional[str] = Field(
        default=None, description="Geographic name (e.g., Canada)"
    )
    DGUID: Optional[str] = Field(
        default=None, description="Detailed geographic unique identifier"
    )

    MEASURE: Optional[str] = Field(
        default=None, description="Type of measurement (e.g., percentage, count)"
    )

    SEX_AT_BIRTH: Optional[str] = Field(
        default=None, description="Sex at birth (e.g., Male, Female)"
    )

    AGE_GROUP: Optional[str] = Field(
        default=None, description="Age group (e.g., 18-34 years)"
    )

    CHARACTERISTICS: Optional[str] = Field(
        default=None, description="Characteristic measured (e.g., symptoms, antibodies)"
    )

    UOM: Optional[str] = Field(
        default=None, description="Unit of measure (e.g., percent)"
    )
    UOM_ID: Optional[int] = Field(default=None, description="Unit of measure ID")

    SCALAR_FACTOR: Optional[str] = Field(
        default=None,
        description="Scalar factor applied to the value (e.g., units, thousands)",
    )
    SCALAR_ID: Optional[int] = Field(default=None, description="Scalar factor ID")

    VECTOR: Optional[str] = Field(
        default=None, description="Internal metadata vector code"
    )
    COORDINATE: Optional[str] = Field(
        default=None, description="Coordinate code used in data"
    )

    VALUE: Optional[float] = Field(
        default=None, description="Reported value of the measure"
    )

    STATUS: Optional[str] = Field(
        default=None, description="Status (e.g., Valid, Suppressed)"
    )
    STATUS_DESCRIPTION: Optional[str] = Field(
        default=None, description="Detailed description of the data status"
    )

    DECIMALS: Optional[int] = Field(
        default=None, description="Number of decimal places in the reported value"
    )
    INGESTION_DATE: Optional[datetime] = Field(
        default=None, description="Timestamp when the data was ingested"
    )
    FILENAME: Optional[str] = Field(
        default=None, description="Source file name from which the data was ingested"
    )
