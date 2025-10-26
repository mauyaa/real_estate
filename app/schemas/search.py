from __future__ import annotations

from typing import List, Sequence

from pydantic import BaseModel, Field


class PolygonCoordinate(BaseModel):
    lat: float = Field(..., description="Latitude in decimal degrees")
    lon: float = Field(..., description="Longitude in decimal degrees")


class PropertyResponse(BaseModel):
    id: str
    title: str
    price_kes: int
    bedrooms: int
    bathrooms: int
    amenities: Sequence[str]
    verified: bool
    commute_minutes_to_cbd: int
    agent_id: str


class PropertySearchRequest(BaseModel):
    polygon: List[PolygonCoordinate] | None = Field(
        None,
        description="Polygon coordinates describing the search area (clockwise or counter-clockwise)",
    )
    max_price: int | None = None
    min_bedrooms: int | None = None
    amenities: Sequence[str] | None = None
    max_commute_minutes: int | None = None
    require_verified: bool = False


class PropertySearchResponse(BaseModel):
    results: Sequence[PropertyResponse]
