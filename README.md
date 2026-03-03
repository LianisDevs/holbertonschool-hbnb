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
 
### AMENITY MANAGEMENT

#### CREATE AMENITY

To Create an amenity, and keeping it clear using the JSON format. Use the below example, while filling the "name" field, with your desired Amenity name.
```
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Your Amenity Name Here"}'
```
```
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Your Second Amenity Name Here"}'

```
**Expected Output**
```
{
  "id": 1,
  "name": "Your Amenity Name Here"
}
{
  "id": 2,
  "name": "Your Second Amenity Name Here"
}
```

#### GET ALL AMENITIES

To get a list of all the current Amenities, you can just use the simple curl command below
```
curl http://127.0.0.1:5000/api/v1/amenities/
```
**Expected Output**
```
[
  {
    "id": 1,
    "name": "Your Amenity Name Here"
  },
  {
    "id": 2,
    "name": "Your Second Amenity Name Here"
  }
]
```

#### GET AMENITY BY ID

To list an amenity based on it's ID, use the following curl command.
```
curl http://127.0.0.1:5000/api/v1/amenities/<1>
```
**Expected Output**
```
{
   "id": 1,
   "name": "Your Amenity Name Here"
 },
```

#### CHANGE THE NAME OF AN AMENITY, USING ID

To change the details of an amenity (name), use the following command.
```
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/1 \
-H "Content-Type: application/json" \
-d '{"name": "Updated Name"}'
```
**Expected Output**
```
{
  "id": 1,
  "name": "Updated Name"
}
```
It is important that you change the "1" ID as this is how you specify which amenity is being changed

# AUTHORS
- **Liani Mckeown**
- **Lachie King**
- **Uliana Deshin**
- **Anthonia Ifoeze**
