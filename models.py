from typing import List

from pydantic import BaseModel, field_validator


class Passenger(BaseModel):
    """
    Data model for passenger details with validation.
    """

    Name: str
    Age: int
    Gender: str

    @field_validator("Name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty.")
        if not v.isalpha():
            raise ValueError("Name must contain only letters.")
        return v.title()

    @field_validator("Age")
    def validate_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError("Age must be between 0 and 120.")
        return v

    @field_validator("Gender")
    def validate_gender(cls, v):
        if v.lower() not in {"male", "female", "other"}:
            raise ValueError("Gender must be 'Male', 'Female', or 'Other'.")
        return v.capitalize()


class BookingData(BaseModel):
    """
    Data model for booking fields with validation using Pydantic.
    """

    UserID: str
    Password: str
    FromStation: str
    ToStation: str
    Date: str
    Class: str
    Quota: str
    MobileNo: str
    Passengers: List[Passenger]

    @field_validator("UserID")
    def validate_user_id(cls, v):
        if not v.strip():
            raise ValueError("UserID cannot be empty.")
        return v

    @field_validator("Password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return v

    @field_validator("FromStation", "ToStation")
    def validate_station(cls, v, field):
        if not v.strip():
            raise ValueError(f"{field.field_name} cannot be empty.")
        if not v.isalpha():
            raise ValueError(f"{field.field_name} must contain only letters.")
        return v.title()

    @field_validator("Date")
    def validate_date(cls, v):
        if len(v) != 10 or v[2] != "-" or v[5] != "-":
            raise ValueError("Date must be in the format DD-MM-YYYY.")
        day, month, year = v.split("-")
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            raise ValueError("Date must contain valid numbers.")
        day, month, year = int(day), int(month), int(year)
        if not (1 <= day <= 31 and 1 <= month <= 12 and year >= 1900):
            raise ValueError("Date contains invalid day, month, or year.")
        return v

    @field_validator("Class")
    def validate_class(cls, v):
        valid_classes = {"1A", "2A", "3A", "SL", "CC", "2S"}
        if v.upper() not in valid_classes:
            raise ValueError(f"Class must be one of {', '.join(valid_classes)}.")
        return v.upper()

    @field_validator("Quota")
    def validate_quota(cls, v):
        valid_quotas = {"GN", "TQ", "LD", "DF", "PH", "FT"}
        if v.upper() not in valid_quotas:
            raise ValueError(f"Quota must be one of {', '.join(valid_quotas)}.")
        return v.upper()

    @field_validator("MobileNo")
    def validate_mobile(cls, v):
        if len(v) != 10 or not v.isdigit():
            raise ValueError("Mobile number must be 10 digits.")
        return v
