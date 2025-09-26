from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from app.models.property import AgentAvailability, GeoPoint, Property


class PropertyRepository:
    """Repository that loads property and availability data from JSON files."""

    def __init__(self, properties_path: Path, availability_path: Path) -> None:
        self._properties_path = properties_path
        self._availability_path = availability_path
        self._properties = self._load_properties()
        self._availability = self._load_availability()

    def _load_properties(self) -> List[Property]:
        with self._properties_path.open() as handle:
            raw_items = json.load(handle)
        properties: List[Property] = []
        for item in raw_items:
            polygon = [GeoPoint(**point) for point in item["polygon"]]
            prop = Property(
                id=item["id"],
                title=item["title"],
                price_kes=item["price_kes"],
                bedrooms=item["bedrooms"],
                bathrooms=item["bathrooms"],
                amenities=tuple(item["amenities"]),
                verified=item["verified"],
                location=GeoPoint(**item["location"]),
                commute_minutes_to_cbd=item["commute_minutes_to_cbd"],
                polygon=polygon,
                agent_id=item["agent_id"],
            )
            properties.append(prop)
        return properties

    def _load_availability(self) -> List[AgentAvailability]:
        with self._availability_path.open() as handle:
            raw_items = json.load(handle)
        return [
            AgentAvailability(agent_id=item["agent_id"], available_slots=tuple(item["available_slots"]))
            for item in raw_items
        ]

    @property
    def properties(self) -> Iterable[Property]:
        return tuple(self._properties)

    @property
    def availability(self) -> Iterable[AgentAvailability]:
        return tuple(self._availability)

    def update_availability(self, updated: AgentAvailability) -> None:
        self._availability = [avail for avail in self._availability if avail.agent_id != updated.agent_id]
        self._availability.append(updated)

    def get_property(self, property_id: str) -> Property | None:
        return next((prop for prop in self._properties if prop.id == property_id), None)
