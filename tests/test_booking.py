from pathlib import Path

import pytest

from app.models.property import AgentAvailability
from app.repositories.property_repository import PropertyRepository
from app.services.booking_service import BookingConflictError, BookingService


def make_service() -> BookingService:
    repo = PropertyRepository(
        properties_path=Path("data/sample_properties.json"),
        availability_path=Path("data/agent_availability.json"),
    )
    return BookingService(repo)


def test_successful_booking_consumes_slot():
    service = make_service()
    booking = service.schedule_viewing(
        property_id="prop-001",
        consumer_name="Grace",
        consumer_phone="0712345678",
        desired_slot="2024-04-10T09:00:00+03:00",
    )
    assert booking.property_id == "prop-001"
    availability = service.availability_for(booking.agent_id)
    assert availability is not None
    assert "2024-04-10T09:00:00+03:00" not in availability.available_slots


def test_booking_same_slot_twice_raises_conflict():
    service = make_service()
    service.schedule_viewing(
        property_id="prop-001",
        consumer_name="Grace",
        consumer_phone="0712345678",
        desired_slot="2024-04-10T09:00:00+03:00",
    )
    with pytest.raises(BookingConflictError):
        service.schedule_viewing(
            property_id="prop-001",
            consumer_name="Ian",
            consumer_phone="0798765432",
            desired_slot="2024-04-10T09:00:00+03:00",
        )


def test_same_slot_different_agents_is_allowed():
    service = make_service()
    service._repository.update_availability(
        AgentAvailability(
            agent_id="agent-kenya-02",
            available_slots=(
                "2024-04-10T09:00:00+03:00",
                "2024-04-12T16:00:00+03:00",
            ),
        )
    )

    first = service.schedule_viewing(
        property_id="prop-001",
        consumer_name="Grace",
        consumer_phone="0712345678",
        desired_slot="2024-04-10T09:00:00+03:00",
    )

    second = service.schedule_viewing(
        property_id="prop-002",
        consumer_name="Ian",
        consumer_phone="0798765432",
        desired_slot="2024-04-10T09:00:00+03:00",
    )

    assert first.agent_id != second.agent_id
    assert first.scheduled_slot == second.scheduled_slot
