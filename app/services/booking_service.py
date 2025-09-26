from __future__ import annotations

import uuid
from typing import Dict, Iterable

from app.models.property import AgentAvailability, Booking
from app.repositories.property_repository import PropertyRepository


class BookingConflictError(Exception):
    pass


class UnknownAgentError(Exception):
    pass


class BookingService:
    def __init__(self, repository: PropertyRepository) -> None:
        self._repository = repository
        self._bookings: Dict[str, Booking] = {}

    def schedule_viewing(
        self,
        property_id: str,
        consumer_name: str,
        consumer_phone: str,
        desired_slot: str,
    ) -> Booking:
        property_ = self._repository.get_property(property_id)
        if property_ is None:
            raise ValueError(f"Unknown property: {property_id}")

        availability = next(
            (avail for avail in self._repository.availability if avail.agent_id == property_.agent_id),
            None,
        )
        if availability is None:
            raise UnknownAgentError(f"No availability for agent {property_.agent_id}")
        if desired_slot not in availability.available_slots:
            raise BookingConflictError("Requested slot is not available")
        if any(
            booking.scheduled_slot == desired_slot and booking.agent_id == property_.agent_id
            for booking in self._bookings.values()
        ):
            raise BookingConflictError("Slot already booked")

        booking = Booking(
            booking_id=str(uuid.uuid4()),
            property_id=property_id,
            agent_id=property_.agent_id,
            consumer_name=consumer_name,
            consumer_phone=consumer_phone,
            scheduled_slot=desired_slot,
        )
        self._bookings[booking.booking_id] = booking

        updated_slots = tuple(slot for slot in availability.available_slots if slot != desired_slot)
        self._repository.update_availability(
            AgentAvailability(agent_id=availability.agent_id, available_slots=updated_slots)
        )
        return booking

    def list_bookings(self) -> Iterable[Booking]:
        return list(self._bookings.values())

    def availability_for(self, agent_id: str) -> AgentAvailability | None:
        return next((avail for avail in self._repository.availability if avail.agent_id == agent_id), None)
