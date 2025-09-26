import pytest

from app.services.payment_service import InsufficientAmountError, PaymentService


def test_record_payment_succeeds():
    service = PaymentService()
    entry = service.record_payment(
        payer="tenant-1",
        payee="agent-kenya-01",
        amount_kes=50000,
        currency="KES",
        type_="rent",
        booking_id="booking-123",
        metadata={"split": "primary"},
    )
    assert entry.amount_kes == 50000
    assert len(list(service.list_entries())) == 1


def test_record_payment_rejects_non_positive_amount():
    service = PaymentService()
    with pytest.raises(InsufficientAmountError):
        service.record_payment(
            payer="tenant-1",
            payee="agent-kenya-01",
            amount_kes=0,
            currency="KES",
            type_="rent",
            booking_id=None,
        )


def test_record_payment_metadata_is_copied():
    service = PaymentService()
    metadata = {"split": "primary", "details": {"method": "mpesa"}}

    entry = service.record_payment(
        payer="tenant-1",
        payee="agent-kenya-01",
        amount_kes=50000,
        currency="KES",
        type_="rent",
        booking_id="booking-immutable",
        metadata=metadata,
    )

    metadata["split"] = "updated"
    metadata["details"]["method"] = "card"

    assert entry.metadata == {"split": "primary", "details": {"method": "mpesa"}}
