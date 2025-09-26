from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence


@dataclass(frozen=True)
class GeoPoint:
    """Simple latitude/longitude coordinate."""

    lat: float
    lon: float


@dataclass(frozen=True)
class Property:
    """Domain entity representing a property listing."""

    id: str
    title: str
    price_kes: int
    bedrooms: int
    bathrooms: int
    amenities: Sequence[str]
    verified: bool
    location: GeoPoint
    commute_minutes_to_cbd: int
    polygon: List[GeoPoint]
    agent_id: str


@dataclass(frozen=True)
class AgentAvailability:
    agent_id: str
    available_slots: Sequence[str]


@dataclass(frozen=True)
class Booking:
    booking_id: str
    property_id: str
    agent_id: str
    consumer_name: str
    consumer_phone: str
    scheduled_slot: str


@dataclass(frozen=True)
class PaymentEntry:
    """Represents a single ledger transaction."""

    entry_id: str
    booking_id: str | None
    payer: str
    payee: str
    amount_kes: int
    currency: str
    type: str
    metadata: dict
