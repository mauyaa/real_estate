"""Booking service module.

Provides thread-safe booking operations with conflict detection and
availability tracking.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from threading import Lock
from typing import Dict, List, Optional


class BookingError(Exception):
    """Base class for booking related errors."""


class BookingConflictError(BookingError):
    """Raised when a booking conflicts with existing reservations."""


class AvailabilityError(BookingError):
    """Raised when a property is unavailable for booking."""


@dataclass(frozen=True)
class Booking:
    """Represents a reservation."""

    booking_id: int
    property_id: str
    start_date: date
    end_date: date
    guest_name: Optional[str] = None


class BookingService:
    """Service responsible for creating bookings.

    The service keeps an in-memory list of bookings and the total capacity per
    property. All operations that mutate the internal state are serialised
    through a lock to avoid race conditions during concurrent access.
    """

    def __init__(self, availability: Optional[Dict[str, int]] = None) -> None:
        self._availability: Dict[str, int] = availability.copy() if availability else {}
        self._bookings: List[Booking] = []
        self._next_booking_id: int = 1
        self._lock = Lock()

    def set_availability(self, property_id: str, capacity: int) -> None:
        """Configure the capacity for a property."""
        if capacity < 0:
            raise ValueError("capacity must be positive")
        with self._lock:
            self._availability[property_id] = capacity

    def is_available(self, property_id: str, start: date, end: date) -> bool:
        """Return True when the property has capacity for the period."""
        self._validate_dates(start, end)
        with self._lock:
            return self._is_available_locked(property_id, start, end)

    def list_bookings(self) -> List[Booking]:
        """Return a copy of the current bookings list."""
        with self._lock:
            return list(self._bookings)

    def book(self, property_id: str, start: date, end: date, *, guest_name: Optional[str] = None) -> Booking:
        """Create a booking if the property is available.

        The method performs an optimistic availability check and then repeats
        the check under a lock to guarantee that only one booking can mutate the
        shared state at a time.
        """

        self._validate_dates(start, end)
        # Early exit to provide quick feedback when there is clearly no
        # availability. The check is repeated inside the lock to avoid races.
        if not self.is_available(property_id, start, end):
            raise BookingConflictError("Property is not available for the requested period")

        with self._lock:
            if not self._is_available_locked(property_id, start, end):
                raise BookingConflictError("Property is not available for the requested period")

            booking = Booking(
                booking_id=self._next_booking_id,
                property_id=property_id,
                start_date=start,
                end_date=end,
                guest_name=guest_name,
            )
            self._next_booking_id += 1
            self._bookings.append(booking)
            return booking

    def _is_available_locked(self, property_id: str, start: date, end: date) -> bool:
        capacity = self._availability.get(property_id, 0)
        if capacity <= 0:
            return False
        active = sum(1 for booking in self._bookings if self._overlaps(booking, property_id, start, end))
        return active < capacity

    @staticmethod
    def _overlaps(booking: Booking, property_id: str, start: date, end: date) -> bool:
        if booking.property_id != property_id:
            return False
        return not (booking.end_date <= start or booking.start_date >= end)

    @staticmethod
    def _validate_dates(start: date, end: date) -> None:
        if start >= end:
            raise ValueError("start must be before end")
