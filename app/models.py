from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LocationDTO:
    lat: Optional[float] = None
    lng: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

@dataclass
class AmenitiesDTO:
    general: List[str] = field(default_factory=list)
    room: List[str] = field(default_factory=list)

@dataclass
class ImageDTO:
    link: Optional[str] = None
    description: Optional[str] = None

@dataclass
class ImagesDTO:
    amenities: Optional[ImageDTO] = field(default_factory=list)
    rooms: Optional[ImageDTO] = field(default_factory=list)
    site: Optional[ImageDTO] = field(default_factory=list)

@dataclass
class HotelDTO:
    id: str
    destination_id: Optional[int] = None
    name: Optional[str] = None
    location: LocationDTO = field(default_factory=LocationDTO)
    description: Optional[str] = None
    amenities: AmenitiesDTO = field(default_factory=AmenitiesDTO)
    images: ImagesDTO = field(default_factory=ImagesDTO)
    booking_conditions: List[str] = field(default_factory=list)