from __future__ import annotations

from typing import Sequence

from pydantic import BaseModel, Field


class BookingRequest(BaseModel):
    property_id: str
    consumer_name: str = Field(..., min_length=2)
    consumer_phone: str = Field(..., min_length=9)
    desired_slot: str


class BookingResponse(BaseModel):
    booking_id: str
    property_id: str
    agent_id: str
    consumer_name: str
    consumer_phone: str
    scheduled_slot: str


class AvailabilityResponse(BaseModel):
    agent_id: str
    available_slots: Sequence[str]
