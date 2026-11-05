from __future__ import annotations
import datetime as dt
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

Status = Literal["scheduled", "completed", "cancelled"]

class AppointmentCreate(BaseModel):
    patient: str = Field(min_length=2, max_length=120)
    doctor: str = Field(min_length=2, max_length=120)
    specialty: str = Field(min_length=2, max_length=100)
    date: dt.date
    time: dt.time
    room: int = Field(ge=1, le=999)
    status: Status = "scheduled"

class AppointmentUpdate(AppointmentCreate):
    pass

class AppointmentPatch(BaseModel):
    patient: str | None = Field(default=None, min_length=2, max_length=120)
    doctor: str | None = Field(default=None, min_length=2, max_length=120)
    specialty: str | None = Field(default=None, min_length=2, max_length=100)
    date: dt.date | None = None
    time: dt.time | None = None
    room: int | None = Field(default=None, ge=1, le=999)
    status: Status | None = None

    @model_validator(mode="after")
    def no_explicit_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError("Нельзя передавать null при частичном обновлении")
        return self

class AppointmentResponse(AppointmentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class AppointmentListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[AppointmentResponse]

class AppointmentStatistics(BaseModel):
    total: int
    scheduled: int
    completed: int
    cancelled: int
    specialties: int

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=60, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
