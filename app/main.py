from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, status

from app import dependencies
from app.schemas.booking import AvailabilityResponse, BookingRequest, BookingResponse
from app.schemas.payment import LedgerResponse, PaymentRequest, PaymentResponse
from app.schemas.search import PropertyResponse, PropertySearchRequest, PropertySearchResponse
from app.services.booking_service import BookingConflictError, BookingService, UnknownAgentError
from app.services.payment_service import InsufficientAmountError, PaymentService
from app.services.search_service import SearchFilters, SearchService

app = FastAPI(
    title="Kenya Real Estate Marketplace API",
    description="Prototype API exposing search, booking, and payments primitives",
    version="0.1.0",
)


@app.post("/search/properties", response_model=PropertySearchResponse)
async def search_properties(
    request: PropertySearchRequest,
    service: SearchService = Depends(dependencies.get_search_service),
) -> PropertySearchResponse:
    polygon = None
    if request.polygon:
        polygon = [(coord.lat, coord.lon) for coord in request.polygon]
    filters = SearchFilters(
        polygon=polygon,
        max_price=request.max_price,
        min_bedrooms=request.min_bedrooms,
        amenities=request.amenities,
        max_commute_minutes=request.max_commute_minutes,
        require_verified=request.require_verified,
    )
    properties = [
        PropertyResponse(
            id=prop.id,
            title=prop.title,
            price_kes=prop.price_kes,
            bedrooms=prop.bedrooms,
            bathrooms=prop.bathrooms,
            amenities=prop.amenities,
            verified=prop.verified,
            commute_minutes_to_cbd=prop.commute_minutes_to_cbd,
            agent_id=prop.agent_id,
        )
        for prop in service.search(filters)
    ]
    return PropertySearchResponse(results=properties)


@app.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    request: BookingRequest,
    service: BookingService = Depends(dependencies.get_booking_service),
) -> BookingResponse:
    try:
        booking = service.schedule_viewing(
            property_id=request.property_id,
            consumer_name=request.consumer_name,
            consumer_phone=request.consumer_phone,
            desired_slot=request.desired_slot,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except BookingConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except UnknownAgentError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return BookingResponse(**booking.__dict__)


@app.get("/bookings", response_model=list[BookingResponse])
async def list_bookings(service: BookingService = Depends(dependencies.get_booking_service)) -> list[BookingResponse]:
    return [BookingResponse(**booking.__dict__) for booking in service.list_bookings()]


@app.get("/agents/{agent_id}/availability", response_model=AvailabilityResponse)
async def get_availability(
    agent_id: str,
    service: BookingService = Depends(dependencies.get_booking_service),
) -> AvailabilityResponse:
    availability = service.availability_for(agent_id)
    if availability is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return AvailabilityResponse(agent_id=availability.agent_id, available_slots=availability.available_slots)


@app.post("/payments/rent", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def record_rent_payment(
    request: PaymentRequest,
    service: PaymentService = Depends(dependencies.get_payment_service),
) -> PaymentResponse:
    try:
        entry = service.record_payment(
            payer=request.payer,
            payee=request.payee,
            amount_kes=request.amount_kes,
            currency=request.currency,
            type_=request.type,
            booking_id=request.booking_id,
            metadata=request.metadata,
        )
    except InsufficientAmountError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return PaymentResponse(**entry.__dict__)


@app.get("/payments/ledger", response_model=LedgerResponse)
async def list_ledger(service: PaymentService = Depends(dependencies.get_payment_service)) -> LedgerResponse:
    entries = [PaymentResponse(**entry.__dict__) for entry in service.list_entries()]
    return LedgerResponse(entries=entries)
