from pathlib import Path

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
