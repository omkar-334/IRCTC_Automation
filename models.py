from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator

from dropdowns import berths, classes, genders, quotas


class Passenger(BaseModel):
    """
    Data model for passenger details with validation.
    """

    Name: str
    Age: int
    Gender: str
    Berth: str

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
        if v not in genders:
            raise ValueError(f"Gender must be {', '.join(genders)}.")
        return v

    @field_validator("Berth")
    def validate_berth(cls, v):
        if v not in berths:
            raise ValueError(f"Berth must be {', '.join(berths)}.")
        return v


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
        return v.title()

    @field_validator("Date")
    def validate_date(cls, v):
        date = datetime.strptime(v, "%Y-%m-%d")
        if date < datetime.now():
            raise ValueError("Choose a future date.")
        return v

    @field_validator("Class")
    def validate_class(cls, v):
        if v not in classes:
            raise ValueError(f"Class must be {', '.join(classes)}.")
        return v

    @field_validator("Quota")
    def validate_quota(cls, v):
        if v not in quotas:
            raise ValueError(f"Quota must be {', '.join(quotas)}.")
        return v

    @field_validator("MobileNo")
    def validate_mobile(cls, v):
        if len(v) != 10 or not v.isdigit():
            raise ValueError("Mobile number must be 10 digits.")
        return v
