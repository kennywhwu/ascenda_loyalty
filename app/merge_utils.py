from app.models import HotelDTO, AmenitiesDTO, ImagesDTO

def merge_hotels(suppliers_data, destination_id=None, hotel_ids=None):
    merged_hotels = {}
    
    for hotels in suppliers_data.values():
        for hotel in hotels:
            # Skip hotels that do not match with passed in destination id or hotel id (prioritize hotel id filter)
            if (hotel_ids and hotel.id not in hotel_ids) or (destination_id and hotel.destination_id != destination_id):
                continue
            if hotel.id not in merged_hotels:
                merged_hotels[hotel.id] = hotel
            else:
                merged_hotels[hotel.id] = merge_hotel_data(merged_hotels[hotel.id], hotel)
    
    return list(merged_hotels.values())

def merge_hotel_data(existing_hotel, new_hotel):
    room_amenities = list(set(existing_hotel.amenities.room + new_hotel.amenities.room))
    # Assuming that any amenities that are not in room are considered "general"
    general_amenities = [amenity for amenity in list(set(existing_hotel.amenities.general + new_hotel.amenities.general)) if amenity not in room_amenities]

    return HotelDTO(
        id=existing_hotel.id,
        destination_id=new_hotel.destination_id or existing_hotel.destination_id,
        name=new_hotel.name or existing_hotel.name,
        location=new_hotel.location if (new_hotel.location.lat and new_hotel.location.lng) else existing_hotel.location,
        description=new_hotel.description or existing_hotel.description,
        amenities=AmenitiesDTO(
            general=general_amenities,
            room=room_amenities,
        ),
        images=ImagesDTO(
            rooms=dedupe_images(existing_hotel.images.rooms + new_hotel.images.rooms),
            site=dedupe_images(existing_hotel.images.site + new_hotel.images.site),
            amenities=dedupe_images(existing_hotel.images.amenities + new_hotel.images.amenities),
        ),
        booking_conditions=list(set(existing_hotel.booking_conditions + new_hotel.booking_conditions)),
    )

def dedupe_images(images):
    deduped_images_dict = {}
    for image in images:
        key_value = image.link
        if key_value not in deduped_images_dict:
            deduped_images_dict[key_value] = image
    return list(deduped_images_dict.values())