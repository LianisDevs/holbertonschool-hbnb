# HBNB
This Repository contains the files for the HBNB project. HBNB replicates the basic functionalities of the AirBNB application, which allows users to find and book short term rentals. These users can also leave reviews on the locations they stay at.

### Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
	- [User](#user)
	- [Place](#place)
	- [Review](#review)
	- [Ammenity](#ammenity)
- [Tests](#tests)
- [Files](#files)
- [Authors](#authors)

# Features
CRUD capabilites for User/ Place/ Review/ Ammenities 
(please note User cannot delete in this version this will be implemented in a future version)

# Requirements
This project requires Python version 3.14 or later. To check what version of Python you have installed use the command below:
```bash
> python --version
```
# Installation
1. Clone the repository locally
```bash
> git clone https://github.com/LianisDevs/holbertonschool-hbnb
```
2. Navigate to this directory
```bash
> cd holbertonschool-hbnb
```
3. Install the dependencies using
```bash
> pip install -r requirements.txt
```

# Usage
Run the application from the holbertonschool-hbnb directory
```bash
> python3 run.py
```
Use tools like Postman or cURL to use the API endpoints, below examples use curl:

## User

#### Testing the Creation of a User
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "is_admin": false
  }'
```

**Expected Response**

```jsonc
{
    "id": "b0fc1e80-e91d-43d0-bb4d-c686952adeff",
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "is_admin": false
}

// 201 Created
```
#### Testing Email Already Registered
First create a user, then attempt to register again with the same email.

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "is_admin": false
  }'
```
**Expected Response**
```jsonc
{
    "error": "Email already registered"
}

// 400 Bad Request
```
#### Testing Invalid Input Data — Missing Required Field
Omitting *first_name* from the request body.
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "is_admin": false
  }'
```
**Expected Response**
```jsonc
{
    "errors": {
        "first_name": "'first_name' is a required property"
    },
    "message": "Input payload validation failed"
}

// 400 Bad Request
```
#### Testing Invalid Input Data — Bad Email Format
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "not-a-valid-email",
    "is_admin": false
  }'
```

**Expected Response**

```jsonc
{
    "error": "User email must be a valid email"
}

// 400 Bad Request
```

### RETRIEVE USERS

#### Testing Retrieval of All Users
```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/"
```
**Expected Response**
```jsonc
[
    {
        "id": "00b803c9-c44a-47d1-b0f2-889528a6f016",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@example.com",
        "is_admin": false
    },
    {
        "id": "11c914d0-d55b-58e2-c1g3-990639b7b127",
        "first_name": "Alice",
        "last_name": "Wonder",
        "email": "alice.wonder@example.com",
        "is_admin": false
    }
]

// 200 OK
```
#### Testing Retrieval of All Users — Empty List
When no users have been created yet.
```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/"
```
**Expected Response**
```jsonc
[]

// 200 OK
```
### SEARCH USER BY ID

#### Testing Get User by ID — Found
Replace <user_id> with a valid user ID returned from a previous creation request.
```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/00b803c9-c44a-47d1-b0f2-889528a6f016"
```
**Expected Response**

```jsonc
{
    "id": "00b803c9-c44a-47d1-b0f2-889528a6f016",
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "is_admin": false
}

// 200 OK
```
#### Testing Get User by ID — Not Found
```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/nonexistent-id-999"
```

**Expected Response**

```jsonc
{
    "error": "User not found"
}

// 404 Not Found
```

#### SEARCH USER BY EMAIL
Testing Get User by Email — Found

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/email/john.smith@example.com"
```
**Expected Response**

```jsonc
{
    "id": "00b803c9-c44a-47d1-b0f2-889528a6f016",
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "is_admin": false
}

// 200 OK
```

#### SEARCH USER BY EMAIL
Testing Get User by Email — Not Found

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/email/john.smithle.com"
```
**Expected Response**

```jsonc
{
    "error": "User not found"
}

// 404 Not Found
```

### UPDATE USER
#### Testing Update a User — Success

Replace <user_id> with a valid user ID returned from a previous creation request.
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/00b803c9-c44a-47d1-b0f2-889528a6f016" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jonathan",
    "last_name": "Smith",
    "email": "jonathan.smith@example.com",
    "is_admin": false
  }'
```

**Expected Response**

```jsonc
{
    "id": "00b803c9-c44a-47d1-b0f2-889528a6f016",
    "first_name": "Jonathan",
    "last_name": "Smith",
    "email": "jonathan.smith@example.com",
    "is_admin": false
}

// 200 OK
```

#### Testing Update a User — User Not Found
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/nonexistent-id-999" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ghost",
    "last_name": "User",
    "email": "ghost@example.com",
    "is_admin": false
  }'
```

**Expected Response**

```jsonc
{
    "error": "User not found"
}

// 404 Not Found
```

#### Testing Update a User — Partial Update
Only fields provided in the body will be updated. Fields omitted keep their existing values.

```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/00b803c9-c44a-47d1-b0f2-889528a6f016" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Johnny"
  }'
```

**Expected Response**

```jsonc
{
    "id": "00b803c9-c44a-47d1-b0f2-889528a6f016",
    "first_name": "Johnny",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "is_admin": false
}

// 200 OK
```
## Place
Before completing these tests, ensure you have a valid user UUID generated from creating a User (found in the User section). You will also need to create two distinct amenities with their own valid ids (create an amenity using instructions from the Amenity section).

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
  **Expected Response:**
```jsonc
{
  "id": "cottage789",
  "title": "Fantabulous Cottage in the Woods",
  "description": "A super cute cottage where you can live out your fairytale dreams!",
  "price": 250.0,
  "latitude": 36.7489,
  "longitude": -119.7722,
  "owner_id": "kittycat500",
  "amenities": ["wifi123", "pool456"],
  "created_at": "2026-03-03T10:30:00.123456",
  "updated_at": "2026-03-03T10:30:00.123456"
}

// 201 Created
```
#### GET ALL PLACES
Get all places as a list with this curl command: 
```bash
curl -X GET http://127.0.0.1:5000/api/v1/places/
```
**Expected Response:**
```jsonc
[
  {
    "id": "cottage789",
    "title": "Fantabulous Cottage in the Woods",
    "description": "A super cute cottage where you can live out your fairytale dreams!",
    "price": 250.0,
    "latitude": 36.7489,
    "longitude": -119.7722,
    "owner": {
      "id": "kittycat500",
      "first_name": "Katrina",
      "last_name": "Catworthy",
      "email": "kitty.cat@example.com"
    },
    "amenities": [
      {
        "id": "wifi123",
        "name": "WiFi"
      }
    ],
    "created_at": "2026-03-03T10:30:00.123456",
    "updated_at": "2026-03-03T10:30:00.123456"
  }
]

// 200 OK
```

#### GET PLACE BY ID
Get a specific place with an id with this curl command (replace cottage789 with a valid place_id):
```bash
curl -X GET http://127.0.0.1:5000/api/v1/places/cottage789
```
**Expected Response:**
```jsonc
{
  "id": "cottage789",
  "title": "Beach House",
  "description": "Beautiful oceanfront property",
  "price": 250.0,
  "latitude": 36.7489,
  "longitude": -119.7722,
  "owner": {
    "id": "kittycat500",
    "first_name": "Katrina",
    "last_name": "Catworthy",
    "email": "kitty.cat@example.com"
  },
  "amenities": [
    {
      "id": "wifi123",
      "name": "WiFi"
    }
  ],
  "created_at": "2026-03-03T10:30:00.123456",
  "updated_at": "2026-03-03T10:30:00.123456"
}

// 200 OK
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
**Expected Response:**
```jsonc
{
  "id": "cottage789",
  "title": "Updated Beach House",
  "description": "Newly renovated oceanfront property",
  "price": 300.0,
  "latitude": 36.7489,
  "longitude": -119.7722,
  "owner_id": "kittycat500",
  "amenities": ["wifi123"],
  "created_at": "2026-03-03T10:30:00.123456",
  "updated_at": "2026-03-03T11:45:00.123456"
}

// 200 OK
```
## Review
#### CREATE A REVIEW
To create a review you need a valid user_id and place_id, make sure you replace the user_id and place_id in the curl command:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
     -H "Content-Type: application/json" \
     -d '{
		"text": "Dream stay, can't wait to go back!",
		"rating": 5, "user_id": <add user_id>,
		"place_id": <add place_id>
		}'
```
Expected response valid data:
```jsonc
{
  "id": "<review_id>",
  "text": "Great place to stay!",
  "rating": 5,
  "user_id": "<user_id",
  "place_id": "<place_id>"
}

// 201 Created
```
Expected response invalid data:
```jsonc
"Invalid input data"

// 400 Bad Request
```
#### UPDATE REVIEW
To update a review you need a valid review_id, make sure you replace the review_id in the curl command:
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/reviews/<review_id> \
     -H "Content-Type: application/json" \
     -d '{"text": "Horrible stay, ", "rating": 1}'
```
Expected response valid data:
```jsonc
{
  "message": "Review updated successfully"
}

// 200 OK
```
Expected response invalid review_id:
```jsonc
"Review not found"

// 404 Not found
```
Expected response invalid review data:
```jsonc
"Invalid input data"

// 400 Bad request
```

#### GET REVIEW BY ID
To get a review by id you need a valid review_id, make sure you replace the review_id in the curl command:
```bash
curl -X GET http://127.0.0.1:5000/api/v1/reviews/<review_id>
```
Expected response valid data:
```jsonc
{
  "id": "<review_id>",
  "text": "Great place to stay!",
  "rating": 5,
  "user_id": "<user_id",
  "place_id": "<place_id>"
}

// 200 OK
```
Expected response invalid review_id:
```jsonc
"Review not found"

// 404 Not found
```
#### GET REVIEWS BY PLACE ID
To get all the reviews for a place you need a valid place_id, make sure you replace the place_id in the curl command:
```bash
curl -X GET http://127.0.0.1:5000/api/v1/places/<place_id>/reviews
```
Expected response valid data:
```jsonc
[
  {
    "id": "<review_id>",
    "text": "Great place to stay!",
    "rating": 5
  },
  ...
]

// 200 OK
```
Expected response invalid place_id:
```jsonc
{
  "error": "Place not found"
}

// 404 Not found
```

#### GET ALL REVIEWS
To get all reviews:
```bash
curl -X GET http://127.0.0.1:5000/api/v1/reviews/
```
Expected response if there's reviews in memory:
```jsonc
[
  {
    "id": "<review_id>",
    "text": "Great place to stay!",
    "rating": 5
  },
  ...
]

// 200 OK
```
Expected response if no reviews in memory:
```jsonc
[]

// 200 OK
```
#### DELETE REVIEW
To delete a review you need a valid review_id, make sure you replace the review_id in the curl command:
```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<review_id>
```
Expected response valid data:
```jsonc
{
  "message": "Review deleted successfully"
}

// 200 OK
```
Expected response invalid review_id:
```jsonc
"Review not found"

// 404 Not found
```
## Ammenity
#### CREATE AMENITY

To Create an amenity, and keeping it clear using the JSON format. Use the below example, while filling the "name" field, with your desired Amenity name.
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Your Amenity Name Here"}'
```
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Your Second Amenity Name Here"}'

```
**Expected Output**
```jsonc
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
```bash
curl http://127.0.0.1:5000/api/v1/amenities/
```
**Expected Output**
```jsonc
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
```bash
curl http://127.0.0.1:5000/api/v1/amenities/<1>
```
**Expected Output**
```jsonc
{
   "id": 1,
   "name": "Your Amenity Name Here"
 },
```

#### CHANGE THE NAME OF AN AMENITY, USING ID

To change the details of an amenity (name), use the following command.
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/1 \
-H "Content-Type: application/json" \
-d '{"name": "Updated Name"}'
```
**Expected Output**
```jsonc
{
  "id": 1,
  "name": "Updated Name"
}
```
It is important that you change the "1" ID as this is how you specify which amenity is being changed

# Tests
This application has been tested using pytest. To run the tests created:
```bash
> cd holberton-hbnb
> pip install pytest
> python3 -m pytest
```
This will create a test session and run all the tests. As of 04/03/2026 there is 58 tests for expected outcomes and errors. 

# Files
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
│   |   ├── __init__.py
│   |   ├── repository.py
│   ├── utils/
│   │   ├── errors/
│   │   ├── __init__.py
│   │       ├── __init__.py
│   │       ├──review_errors.py
│   ├── tests/
│   │   ├── api/
│   │		├── ammenity_test.py
│   │   ├── models/
│   │		├── model_test.py
│   │   ├── services/
│   │		├── facade_test.py
│   │		├── place_test.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```


#### APP
* The app/ directory contains the core application code

#### API
* The api/ subdirectory houses the API endpoint, organised by version

* v1
    * reviews.py
    * users.py
    * places.py
    * ammenities.py

* __init__.py
    * This tells python to treat these directories as importable packages

#### MODELS
* The models/ subdirectory contains the business logic classes
    * __init__.py
    * amenity.py
    * place.py
    * review.py
    * user.py

#### PERSISTENCE
* The persistence/ subdirectory is where the in-memory repository is implemented. Later version will replace with a database using SQL Alchemy
    * __init__.py
    * repository.py

#### SERVICES
* The services/ subdirectory is where the facade pattern is implemented. Managing the interaction between layers
    * __init__.py
    * facade.py

#### TESTS
* The tests/ subdirectory contains the pytest tests for this project

#### UTILS
* The utils/ subdirectory houses the custom errors
    * __init__.py
    * errors/
		* __init__.py
		* review_errors.py
* config.py
    * This will be used for configuring enviornment variables and application settings
	
* requirements.txt
    * This will list all the python packages needed for the project

* run.py
    * This is the entry point for running the Flask application

# AUTHORS
- **Liani Mckeown**
- **Lachie King**
- **Uliana Deshin**
- **Anthonia Ifoeze**
