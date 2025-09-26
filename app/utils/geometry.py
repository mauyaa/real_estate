from __future__ import annotations

from typing import Iterable

from app.models.property import GeoPoint


def point_in_polygon(point: GeoPoint, polygon: Iterable[GeoPoint]) -> bool:
    """Ray casting algorithm for testing whether a point lies within a polygon."""

    poly = list(polygon)
    if len(poly) < 3:
        return False

    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        pi = poly[i]
        pj = poly[j]
        intersects = (
            ((pi.lon > point.lon) != (pj.lon > point.lon))
            and (
                point.lat
                < (pj.lat - pi.lat) * (point.lon - pi.lon) / (pj.lon - pi.lon + 1e-12) + pi.lat
            )
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def centroid(polygon: Iterable[GeoPoint]) -> GeoPoint:
    poly = list(polygon)
    if not poly:
        raise ValueError("Polygon must not be empty")
    lat = sum(p.lat for p in poly) / len(poly)
    lon = sum(p.lon for p in poly) / len(poly)
    return GeoPoint(lat=lat, lon=lon)
