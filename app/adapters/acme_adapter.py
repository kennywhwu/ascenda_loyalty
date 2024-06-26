import requests
from app.adapters.base_adapter import BaseAdapter
from app.models import HotelDTO, LocationDTO, AmenitiesDTO

class AcmeAdapter(BaseAdapter):
    def fetch_data(self):
        response = requests.get("https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme")
        data = response.json()
        return [self._to_dto(hotel) for hotel in data]

    def _to_dto(self, hotel):
        location = LocationDTO(
            lat=hotel.get("Latitude") or None,
            lng=hotel.get("Longitude") or None,
            address=f"{(hotel.get("Address", "") or "").strip()}, {hotel.get("PostalCode")}",
            city=hotel.get("City"),
            country=hotel.get("Country"),
        )

        amenities = AmenitiesDTO(
            general=[amenity.replace(" ", "").lower() for amenity in hotel.get("Facilities", []) or []],
        )

        return HotelDTO(
            id=hotel.get("Id"),
            destination_id=hotel.get("DestinationId"),
            name=hotel.get("Name"),
            location=location,
            description=hotel.get("Description", "").strip(),
            amenities=amenities,
        )
