from __future__ import annotations

from typing import Sequence

from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    payer: str
    payee: str
    amount_kes: int = Field(..., gt=0)
    currency: str = Field(default="KES")
    type: str = Field(default="rent")
    booking_id: str | None = None
    metadata: dict | None = None


class PaymentResponse(BaseModel):
    entry_id: str
    booking_id: str | None
    payer: str
    payee: str
    amount_kes: int
    currency: str
    type: str
    metadata: dict


class LedgerResponse(BaseModel):
    entries: Sequence[PaymentResponse]
