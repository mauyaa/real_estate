import threading
from typing import List

import pytest

from booking import (
    BookingConflictError,
    BookingService,
    SlotUnavailableError,
)


@pytest.fixture
def service() -> BookingService:
    svc = BookingService()
    svc.add_availability("agent-1", "2025-01-01T09:00")
    return svc


def test_successful_booking_consumes_availability(service: BookingService) -> None:
    booking = service.book("agent-1", "2025-01-01T09:00", "customer-1")

    assert booking.customer_id == "customer-1"
    assert not service.is_available("agent-1", "2025-01-01T09:00")
    assert service.has_conflict("agent-1", "2025-01-01T09:00")


def test_conflicting_booking_is_rejected(service: BookingService) -> None:
    service.book("agent-1", "2025-01-01T09:00", "customer-1")

    with pytest.raises(BookingConflictError):
        service.book("agent-1", "2025-01-01T09:00", "customer-2")


class ThreadResult:
    def __init__(self) -> None:
        self.successful: List[str] = []
        self.failures: List[BaseException] = []
        self.lock = threading.Lock()

    def record_success(self, customer_id: str) -> None:
        with self.lock:
            self.successful.append(customer_id)

    def record_failure(self, exc: BaseException) -> None:
        with self.lock:
            self.failures.append(exc)


def test_multithreaded_conflict_protection() -> None:
    service = BookingService()
    service.add_availability("agent-1", "2025-01-01T09:00")

    barrier = threading.Barrier(2)
    results = ThreadResult()

    def attempt_booking(customer: str) -> None:
        try:
            barrier.wait()
            booking = service.book("agent-1", "2025-01-01T09:00", customer)
        except (BookingConflictError, SlotUnavailableError) as exc:
            results.record_failure(exc)
        else:
            results.record_success(booking.customer_id)

    threads = [threading.Thread(target=attempt_booking, args=(customer,)) for customer in ("customer-1", "customer-2")]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(results.successful) == 1
    assert len(results.failures) == 1
