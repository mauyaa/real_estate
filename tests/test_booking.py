from datetime import date
import threading

import pytest

from app.services.booking_service import (
    BookingConflictError,
    BookingService,
)


def test_concurrent_bookings_only_one_succeeds():
    service = BookingService({"villa-1": 1})
    start = date(2024, 5, 1)
    end = date(2024, 5, 10)

    barrier = threading.Barrier(2)
    results = []

    def attempt_booking(idx: int) -> None:
        barrier.wait()
        try:
            booking = service.book("villa-1", start, end, guest_name=f"guest-{idx}")
        except BookingConflictError:
            results.append("conflict")
        else:
            results.append(f"success-{booking.booking_id}")

    threads = [threading.Thread(target=attempt_booking, args=(i,)) for i in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    successes = [result for result in results if result.startswith("success")] \
        if results else []
    conflicts = [result for result in results if result == "conflict"] if results else []

    assert len(results) == 2
    assert len(successes) == 1
    assert len(conflicts) == 1

    # The booking stored in the service should match the successful attempt.
    all_bookings = service.list_bookings()
    assert len(all_bookings) == 1
    assert all_bookings[0].booking_id == int(successes[0].split("-")[-1])
