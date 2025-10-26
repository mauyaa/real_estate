from __future__ import annotations

import copy
import uuid
from typing import Dict, Iterable

from app.models.property import PaymentEntry


class InsufficientAmountError(Exception):
    pass


class PaymentService:
    def __init__(self) -> None:
        self._ledger: Dict[str, PaymentEntry] = {}

    def record_payment(
        self,
        payer: str,
        payee: str,
        amount_kes: int,
        currency: str,
        type_: str,
        booking_id: str | None,
        metadata: dict | None = None,
    ) -> PaymentEntry:
        if amount_kes <= 0:
            raise InsufficientAmountError("Amount must be positive")
        metadata_copy = copy.deepcopy(metadata) if metadata is not None else {}
        entry = PaymentEntry(
            entry_id=str(uuid.uuid4()),
            booking_id=booking_id,
            payer=payer,
            payee=payee,
            amount_kes=amount_kes,
            currency=currency,
            type=type_,
            metadata=metadata_copy,
        )
        self._ledger[entry.entry_id] = entry
        return entry

    def list_entries(self) -> Iterable[PaymentEntry]:
        return list(self._ledger.values())
