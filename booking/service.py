"""Core booking service implementation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set
import threading


class BookingConflictError(RuntimeError):
    """Raised when an attempt to create a booking conflicts with an existing one."""


class SlotUnavailableError(RuntimeError):
    """Raised when an agent has no availability for the requested slot."""


@dataclass(frozen=True)
class Booking:
    """Represents a booking allocation for an agent."""

    agent_id: str
    slot: str
    customer_id: str


class BookingService:
    """Provides a simple in-memory booking implementation with concurrency guarantees."""

    def __init__(self) -> None:
        self._availability: Dict[str, Set[str]] = {}
        self._bookings: Dict[str, List[Booking]] = {}
        self._lock = threading.Lock()

    def set_availability(self, agent_id: str, slots: Iterable[str]) -> None:
        """Define the exact set of available slots for an agent."""
        with self._lock:
            self._availability[agent_id] = set(slots)

    def add_availability(self, agent_id: str, slot: str) -> None:
        """Add a single availability slot for an agent."""
        with self._lock:
            self._availability.setdefault(agent_id, set()).add(slot)

    def has_conflict(self, agent_id: str, slot: str) -> bool:
        """Determine whether the given agent already has a booking for the slot."""
        with self._lock:
            return self._has_conflict_unlocked(agent_id, slot)

    def list_bookings(self, agent_id: Optional[str] = None) -> List[Booking]:
        """Return a copy of the bookings for the given agent or all bookings."""
        with self._lock:
            if agent_id is None:
                return [booking for bookings in self._bookings.values() for booking in bookings]
            return list(self._bookings.get(agent_id, ()))

    def is_available(self, agent_id: str, slot: str) -> bool:
        """Check if the agent has the requested slot available."""
        with self._lock:
            return slot in self._availability.get(agent_id, set())

    def book(self, agent_id: str, slot: str, customer_id: str) -> Booking:
        """Attempt to create a booking for the agent."""
        # Perform an optimistic conflict check to fail fast when possible.
        if self.has_conflict(agent_id, slot):
            raise BookingConflictError(f"Agent {agent_id} already has a booking for slot {slot}.")

        with self._lock:
            available_slots = self._availability.get(agent_id, set())
            if slot not in available_slots:
                raise SlotUnavailableError(
                    f"Agent {agent_id} is not available for slot {slot}."
                )

            if self._has_conflict_unlocked(agent_id, slot):
                raise BookingConflictError(
                    f"Agent {agent_id} already has a booking for slot {slot}."
                )

            booking = Booking(agent_id=agent_id, slot=slot, customer_id=customer_id)
            self._bookings.setdefault(agent_id, []).append(booking)
            available_slots.remove(slot)
            if not available_slots:
                # Keep our internal dict tidy by removing empty availability entries.
                self._availability.pop(agent_id, None)
            return booking

    # Internal helpers -------------------------------------------------
    def _has_conflict_unlocked(self, agent_id: str, slot: str) -> bool:
        bookings = self._bookings.get(agent_id, ())
        return any(existing.slot == slot for existing in bookings)
