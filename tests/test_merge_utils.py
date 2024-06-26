import unittest
from app.merge_utils import merge_hotels, merge_hotel_data
from app.models import HotelDTO, LocationDTO, AmenitiesDTO, ImageDTO, ImagesDTO

class TestMergeUtils(unittest.TestCase):
    def setUp(self):
        self.hotel1 = HotelDTO(
            id='1',
            destination_id=100,
            name='Hotel A',
            location=LocationDTO(lat=1.0, lng=1.0, address='Address A', city='City A', country='Country A'),
            description='Description A',
            amenities=AmenitiesDTO(general=['pool', 'wifi'], room=['tv', 'aircon']),
            images=ImagesDTO(
                rooms=[ImageDTO(link="link1", description="Room 1")],
                site=[ImageDTO(link="link2", description="Site 1")],
                amenities=[ImageDTO(link="link3", description="Amenity 1")],
            ),
            booking_conditions=['Condition 1']
        )

        self.hotel2 = HotelDTO(
            id='1',
            destination_id=100,
            name='Hotel A Updated',
            location=LocationDTO(lat=2.0, lng=2.0, address='Address A Updated', city='City A', country='Country A'),
            description='Description A Updated',
            amenities=AmenitiesDTO(general=['spa', 'wifi'], room=['minibar', 'aircon']),
            images=ImagesDTO(
                rooms=[ImageDTO(link="link4", description="Room 2")],
                site=[ImageDTO(link="link5", description="Site 2")],
                amenities=[ImageDTO(link="link6", description="Amenity 2")],
            ),
            booking_conditions=['Condition 2']
        )

        self.hotel3 = HotelDTO(
            id='2',
            destination_id=200,
            name='Hotel B',
            location=LocationDTO(lat=3.0, lng=3.0, address='Address B', city='City B', country='Country B'),
            description='Description B',
            amenities=AmenitiesDTO(general=['gym', 'wifi'], room=['tv', 'aircon']),
            images=ImagesDTO(
                rooms=[ImageDTO(link="link7", description="Room 3")],
                site=[ImageDTO(link="link8", description="Site 3")],
                amenities=[ImageDTO(link="link9", description="Amenity 3")],
            ),
            booking_conditions=['Condition 3']
        )

    def test_merge_hotel_data(self):
        merged = merge_hotel_data(self.hotel1, self.hotel2)
        self.assertEqual(merged.name, 'Hotel A Updated')
        self.assertEqual(merged.description, 'Description A Updated')
        self.assertIn('spa', merged.amenities.general)
        self.assertIn('pool', merged.amenities.general)
        self.assertIn('tv', merged.amenities.room)
        self.assertIn('minibar', merged.amenities.room)
        self.assertEqual(len(merged.images.rooms), 2)
        self.assertEqual(len(merged.booking_conditions), 2)

    def test_merge_hotels(self):
        suppliers_data = {
            "acme": [self.hotel1, self.hotel3],
            "patagonia": [self.hotel2]
        }
        merged_hotels = merge_hotels(suppliers_data)
        self.assertEqual(len(merged_hotels), 2)
        self.assertTrue(any(hotel.id == '1' for hotel in merged_hotels))
        self.assertTrue(any(hotel.id == '2' for hotel in merged_hotels))

if __name__ == '__main__':
    unittest.main()
