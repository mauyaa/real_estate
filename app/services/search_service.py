from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from app.models.property import GeoPoint, Property
from app.repositories.property_repository import PropertyRepository
from app.utils.geometry import centroid, point_in_polygon


@dataclass
class SearchFilters:
    polygon: Sequence[tuple[float, float]] | None = None
    max_price: int | None = None
    min_bedrooms: int | None = None
    amenities: Sequence[str] | None = None
    max_commute_minutes: int | None = None
    require_verified: bool = False


class SearchService:
    def __init__(self, repository: PropertyRepository) -> None:
        self._repository = repository

    def search(self, filters: SearchFilters) -> Iterable[Property]:
        properties = self._repository.properties

        def matches(property_: Property) -> bool:
            if filters.max_price is not None and property_.price_kes > filters.max_price:
                return False
            if filters.min_bedrooms is not None and property_.bedrooms < filters.min_bedrooms:
                return False
            if filters.amenities is not None and not set(filters.amenities).issubset(
                set(property_.amenities)
            ):
                return False
            if (
                filters.max_commute_minutes is not None
                and property_.commute_minutes_to_cbd > filters.max_commute_minutes
            ):
                return False
            if filters.require_verified and not property_.verified:
                return False
            if filters.polygon is not None:
                search_polygon = [GeoPoint(lat=lat, lon=lon) for lat, lon in filters.polygon]
                if len(search_polygon) < 3:
                    return False
                if not point_in_polygon(centroid(property_.polygon), search_polygon):
                    return False
            return True

        return [prop for prop in properties if matches(prop)]
