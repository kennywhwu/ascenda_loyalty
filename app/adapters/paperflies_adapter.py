import requests
from app.adapters.base_adapter import BaseAdapter
from app.models import HotelDTO, LocationDTO, AmenitiesDTO, ImageDTO, ImagesDTO

class PaperfliesAdapter(BaseAdapter):
    def fetch_data(self):
        response = requests.get("https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies")
        data = response.json()
        return [self._to_dto(hotel) for hotel in data]

    def _to_dto(self, hotel):
        location = LocationDTO(
            address=(hotel.get("location", {}).get("address", "") or "").strip(),
            country=hotel.get("location", {}).get("country", ""),
        )

        room_amenities = [amenity.replace(" ", "").lower() for amenity in hotel.get("amenities", {}).get("room", []) or []]
        general_amenities = [amenity.replace(" ", "").lower() for amenity in hotel.get("amenities", {}).get("general", []) or [] if amenity.replace(" ", "").lower() not in room_amenities]

        amenities = AmenitiesDTO(
            general=general_amenities,
            room=room_amenities,
        )

        rooms_images = []
        for image in hotel.get("images", {}).get("rooms", []):
            rooms_images.append(ImageDTO(link=image["link"], description=image["caption"]))

        site_images = []
        for image in hotel.get("images", {}).get("site", []):
            rooms_images.append(ImageDTO(link=image["link"], description=image["caption"]))

        images = ImagesDTO(
            rooms=rooms_images,
            site=site_images,
        )
        
        return HotelDTO(
            id=hotel.get("hotel_id"),
            destination_id=hotel.get("destination_id"),
            name=hotel.get("hotel_name"),
            location=location,
            description=hotel.get("details", "").strip(),
            amenities=amenities,
            images=images,
            booking_conditions=hotel.get("booking_conditions", []),
        )
