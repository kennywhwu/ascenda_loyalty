# Hotel Merge App

## Introduction

The Hotel Merge App cleans and merges hotel data from multiple suppliers with an API endpoint for querying the hotels. This app fetches hotel data from three suppliers with optional filter parameters, normalizes the data, merges it, and provides an endpoint for querying the merged data.

## Installation

1. Clone the repository:

  ```bash
  git clone https://github.com/kennywhwu/ascenda_loyalty.git
  cd ascenda_loyalty
  ```

2. Create a virtual environment and activate it:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

3. Install the dependencies:

  ```bash
  pip install -r requirements.txt
  ```

## Running the Application

1. Navigate to the hotel_merge_app directory:

  ```bash
  cd ascenda_loyalty
  ```

2. Run the Flask application:

  ```bash
  python app/main.py
  ```

The application will be running at http://127.0.0.1:5000.

## API Endpoint

`GET /hotels`

Fetches merged hotel data based on the provided filters.

### Request Parameters

destination (optional): Filter by destination ID.
hotels (optional): Filter by a list of hotel IDs.

If both destination and hotels parameters are passed, the filtering logic applies tighter exclusion on hotel ids.  If there are no hotels that satisfy both parameters, then no hotels will be returned.

Example Request

  ```bash
  curl http://127.0.0.1:5000/hotels
  ```

Example Response

  ```json
  [
    {
      "id": "iJhz",
      "destination_id": 5432,
      "name": "Beach Villas Singapore",
      "location": {
        "lat": 1.264751,
        "lng": 103.824006,
        "address": "8 Sentosa Gateway, Beach Villas, 098269",
        "city": "Singapore",
        "country": "Singapore"
      },
      "description": "Surrounded by tropical gardens...",
      "amenities": {
        "general": ["outdoorpool", "indoorpool", "businesscenter", "childcare", "wifi", "drycleaning", "breakfast"],
        "room": ["aircon", "tv", "coffee machine", "kettle", "hair dryer", "iron", "bathtub"]
      },
      "images": {
        "rooms": [
          { "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/2.jpg", "description": "Double room" },
          { "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/3.jpg", "description": "Double room" },
          { "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/4.jpg", "description": "Bathroom" }
        ],
        "site": [
          { "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/1.jpg", "description": "Front" }
        ],
        "amenities": [
          { "link": "https://d2ey9sqrvkqdfs.cloudfront.net/0qZF/0.jpg", "description": "RWS" }
        ]
      },
      "booking_conditions": [
        "All children are welcome...",
        "Pets are not allowed.",
        "WiFi is available in all areas and is free of charge.",
        "Free private parking is possible on site..."
      ]
    }
  ]
  ```

## Running Tests

To run the unit tests, execute the following command in the project root directory:

  ```bash
  python -m unittest
  ```

## Design Decisions

- Adapter Pattern: Each supplier has its own adapter class that handles fetching and normalizing data specific to the supplier.
- DTOs: Data Transfer Objects are used to standardize the hotel data structure across different suppliers.
- Merge Logic: The merge logic combines hotel data from different suppliers, prioritizing non-null fields from the latest supplier data. 
  - Amenities are normalized by removing whitespace and setting to lowercase for easier merging. Dedupe logic assumes that amenities that are not set to "room" are considered in "general" category
  - Images are deduped based on url

## Future Improvements

- Additional cleaning logic: Implement more complex logic for clearer and more accurate depiction of merged data
- Caching: Implement caching to reduce redundant data fetching and improve performance.
- Deployment: Create deployment scripts for different environments (e.g., Docker, AWS).
