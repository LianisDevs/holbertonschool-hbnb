# HBNB
---
This Repository contains the files for the HBNB project. HBNB replicates the basic functionalities of the AirBNB application, which allows users to find and book short term rentals. These users can also leave reviews on the locations they stay at.
```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```
config.py
This will be used for configuring enviornment variables and application settings

requirements.txt
This will list all the python packages needed for the project

run.py
This is the entry point for running the Flask application

# APP
The app/ directory contains the core application code

### API
The api/ subdirectory houses the API endpoint, organised by version

v1
current version - 16/02/26

__init__.py
This tells python to treat these directories as importable packages

### MODELS
The models/ subdirectory contains the business logic classes

__init__.py

amenity.py

place.py

review.py

user.py

### PERSISTENCE
The persistence/ subdirectory is where the in-memory repository is implemented. Later version will replace with a database using SQL Alchemy

__init__.py

repository.py

### SERVICES
The services/ subdirectory is where the facade pattern is implemented. Managing the interaction between layers 

__init__.py

facade.py

# INSTALLATION
---
Install the dependencies using:
```
pip install -r requirements.txt
```
# INSTRUCTIONS
### PLACE MANAGEMENT

#### CREATE PLACE
To create a Place using the JSON format, you can use the below example. Fill in the required fields within acceptable ranges. 

Requirements: 
- Title must be a string equal to or below 100 chars
- Description is optional, and must be a string if added
- Price must be a positive integer
- Latitude must be between 90 and -90
- Longitude must be between 180 and -180
- Owner_id must be pre-existing and valid (this can be achieved by creating a user beforehand and copying its provided UUID)
- Any amenities added must be valid (achieve this by completing the 'Create Amenity' instructions below).

Use the curl command below:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fantabulous Cottage in the Woods",
    "description": "A super cute cottage where you can live out your fairytale dreams!",	
    "price": 250.00,
    "latitude": 36.7489,
    "longitude": -119.7722,
    "owner_id": "YOUR_ACTUAL_USER_ID_HERE",
    "amenities": ["YOUR_ACTUAL_WIFI_ID_HERE", "YOUR_ACTUAL_POOL_ID_HERE"]
  }'
  ```
#### GET ALL PLACES
Get all places as a list with this curl command: 
```bash
curl -X GET http://127.0.0.1:5000/api/v1/places/
```

#### GET PLACE BY ID
Get a specific place with an id with this curl command (replace cottage789 with a valid place_id):
```bash
curl -X GET http://127.0.0.1:5000/api/v1/places/cottage789
```

#### UPDATE PLACE
Update an existing place with the fields that require change.
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/places/cottage789 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Beach House",
    "description": "Newly renovated oceanfront property",
    "price": 300.00
  }'
```

### AMENITY MANAGEMENT

#### CREATE AMENITY

To Create an amenity, and keeping it clear using the JSON format. Use the below example, while filling the "name" field, with your desired Amenity name.
```
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Your Amenity Name Here"}'

```

#### GET ALL AMENITIES

To get a list of all the current Amenities, you can just use the simple curl command below
```
curl http://127.0.0.1:5000/api/v1/amenities/
```

#### GET AMENITY BY ID

To list an amenity based on it's ID, use the following curl command.
```
curl http://127.0.0.1:5000/api/v1/amenities/<AMENITY_ID>
```

#### CHANGE THE NAME OF AN AMENITY, USING ID

To change the details of an amenity (name), use the following command.
```
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/<AMENITY_ID> \
-H "Content-Type: application/json" \
-d '{"name": "Updated Name"}'
```
It is important that you change the <AMENITY_ID> field as this is how you specify which amenity is being changed

# AUTHORS
- Liani Mckeown
- Lachie King
- Uliana Deshin
- Anthonia Ifoeze
