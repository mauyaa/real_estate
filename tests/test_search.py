from pathlib import Path

from app.models.property import GeoPoint, Property
from app.repositories.property_repository import PropertyRepository
from app.services.search_service import SearchFilters, SearchService


def test_polygon_and_price_filters_limit_results():
    repo = PropertyRepository(
        properties_path=Path("data/sample_properties.json"),
        availability_path=Path("data/agent_availability.json"),
    )
    service = SearchService(repo)

    filters = SearchFilters(
        polygon=[(-1.2930, 36.7790), (-1.2930, 36.7850), (-1.2910, 36.7850), (-1.2910, 36.7790)],
        max_price=90000,
        require_verified=True,
    )
    results = list(service.search(filters))
    assert len(results) == 1
    assert results[0].id == "prop-001"


def test_polygon_filter_uses_property_location():
    class InMemoryRepo:
        def __init__(self, properties):
            self._properties = tuple(properties)

        @property
        def properties(self):
            return self._properties

    irregular_property = Property(
        id="irregular-001",
        title="Irregular Parcel",
        price_kes=120000,
        bedrooms=3,
        bathrooms=2,
        amenities=("parking",),
        verified=True,
        location=GeoPoint(lat=-1.2995, lon=36.8005),
        commute_minutes_to_cbd=20,
        polygon=[
            GeoPoint(lat=-1.300, lon=36.800),
            GeoPoint(lat=-1.296, lon=36.800),
            GeoPoint(lat=-1.296, lon=36.804),
            GeoPoint(lat=-1.297, lon=36.804),
            GeoPoint(lat=-1.297, lon=36.801),
            GeoPoint(lat=-1.303, lon=36.801),
            GeoPoint(lat=-1.303, lon=36.805),
            GeoPoint(lat=-1.300, lon=36.805),
        ],
        agent_id="agent-concave",
    )
    service = SearchService(InMemoryRepo([irregular_property]))

    filters = SearchFilters(
        polygon=[
            (-1.3005, 36.8000),
            (-1.3005, 36.8010),
            (-1.2990, 36.8010),
            (-1.2990, 36.8000),
        ]
    )

    results = list(service.search(filters))

    assert [prop.id for prop in results] == ["irregular-001"]
