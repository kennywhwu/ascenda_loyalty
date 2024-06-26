import requests
from app.adapters.base_adapter import BaseAdapter
from app.models import HotelDTO, LocationDTO, AmenitiesDTO, ImageDTO, ImagesDTO

class PatagoniaAdapter(BaseAdapter):
    def fetch_data(self):
        response = requests.get("https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia")
        data = response.json()
        return [self._to_dto(hotel) for hotel in data]

    def _to_dto(self, hotel):
        location = LocationDTO(
            lat=hotel.get("lat") or None,
            lng=hotel.get("lng") or None,
            address=(hotel.get("address", "") or "").strip(),
        )

        amenities = AmenitiesDTO(
            general=[amenity.replace(" ", "").lower() for amenity in hotel.get("amenities", []) or []],
        )

        amenities_images = []
        for image in hotel.get("images", {}).get("amenities", []):
            amenities_images.append(ImageDTO(link=image["url"], description=image["description"]))

        rooms_images = []
        for image in hotel.get("images", {}).get("rooms", []):
            rooms_images.append(ImageDTO(link=image["url"], description=image["description"]))

        images = ImagesDTO(
            amenities=amenities_images,
            rooms=rooms_images,
        )

        return HotelDTO(
            id=hotel.get("id"),
            destination_id=hotel.get("destination"),
            name=hotel.get("name"),
            location=location,
            description=(hotel.get("info", "") or "").strip(),
            amenities=amenities,
            images=images,
        )
