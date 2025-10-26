from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from app.repositories.property_repository import PropertyRepository
from app.services.booking_service import BookingService
from app.services.payment_service import PaymentService
from app.services.search_service import SearchService


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@lru_cache(maxsize=1)
def get_repository() -> PropertyRepository:
    return PropertyRepository(
        properties_path=DATA_DIR / "sample_properties.json",
        availability_path=DATA_DIR / "agent_availability.json",
    )


@lru_cache(maxsize=1)
def get_search_service() -> SearchService:
    return SearchService(get_repository())


@lru_cache(maxsize=1)
def get_booking_service() -> BookingService:
    return BookingService(get_repository())


@lru_cache(maxsize=1)
def get_payment_service() -> PaymentService:
    return PaymentService()
