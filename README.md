# Real Estate Marketplace Prototype

This repository provides a FastAPI prototype that demonstrates core flows for the Kenya-focused real estate platform:

- Polygon-aware property search with commute time, amenity, and verification filters.
- Viewing bookings that respect agent availability and prevent double-booking.
- Rent payments recorded in a ledger with validation of amounts and metadata.

## Getting Started

1. Create a virtual environment and install dependencies (either with `pip` or Poetry).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn[standard] pydantic pytest httpx
```

Alternatively install via Poetry:

```bash
poetry install
```

2. Run the API locally:

```bash
uvicorn app.main:app --reload
```

The interactive docs will be available at <http://127.0.0.1:8000/docs>.

## Running Tests

```bash
pytest
```

## Project Structure

- `app/` – FastAPI application, domain models, services, and schemas.
- `data/` – Sample listings and agent availability data that power the prototype.
- `docs/` – Product and architecture documentation for the broader platform vision.
- `tests/` – Unit tests covering search, booking, and payment behaviours.
