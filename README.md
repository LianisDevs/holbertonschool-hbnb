# HBNB
This Repository contains the files for the HBNB project. HBNB replicates the basic functionalities of the AirBNB application, which allows users to find and book short term rentals. These users can also leave reviews on the locations they stay at.

### Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)
- [Authors](#authors)
---
# Features
* CRUD capabilites for User/ Place/ Review/ Ammenities (please note User, Place and Ammenities cannot delete in this version this will be implemented in a future version)



# Requirements

This project requires Python version 3.14 or later. To check what version of Python you have installed use the command below:
```
> python --version
```

# Installation
1. Clone the repository locally
```
> git clone https://github.com/LianisDevs/holbertonschool-hbnb
```
2. Navigate to this directory
```
> cd holbertonschool-hbnb
```
3. Install the dependencies using
```
> pip install -r requirements.txt
```

# Usage
Run the application
```
> python3 run.py
```
Use tools like Postman or cURL to use the API endpoints, below examples use curl:
### CREATE A USER


### CREATE A PLACE


### CREATE A REVIEW
To create a review you need a valid user_id and place_id, make sure you replace the user_id and place_id in the curl command:
```
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
     -H "Content-Type: application/json" \
     -d '{"text": "Dream stay, can't wait to go back!", "rating": 5, "user_id": <add user_id>, "place_id": <add place_id>}'
```
Expected response valid data:
```
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
```
"Invalid input data"

// 400 Bad Request
```
### UPDATE REVIEW
To update a review you need a valid review_id, make sure you replace the review_id in the curl command:
```
curl -X PUT http://127.0.0.1:5000/api/v1/reviews/<review_id> \
     -H "Content-Type: application/json" \
     -d '{"text": "Horrible stay, ", "rating": 1}'
```
Expected response valid data:
```
{
  "message": "Review updated successfully"
}

// 200 OK
```
Expected response invalid review_id:
```
"Review not found"

// 404 Not found
```
Expected response invalid review data:
```
"Invalid input data"

// 400 Bad request
```

### GET REVIEW BY ID
To get a review by id you need a valid review_id, make sure you replace the review_id in the curl command:
```
curl -X GET http://127.0.0.1:5000/api/v1/reviews/<review_id>
```
Expected response valid data:
```
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
```
"Review not found"

// 404 Not found
```
### GET ALL REVIEWS
To get all reviews:
```
curl -X GET http://127.0.0.1:5000/api/v1/reviews/
```
Expected response if there's reviews in memory:
```
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
```
[]

// 200 OK
```
### DELETE REVIEW
To delete a review you need a valid review_id, make sure you replace the review_id in the curl command:
```
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<review_id>
```
Expected response valid data:
```
{
  "message": "Review deleted successfully"
}

// 200 OK
```
Expected response invalid review_id:
```
"Review not found"

// 404 Not found
```

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
│   │   ├── services/
│   │		├── facade_test.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```
* config.py
    * This will be used for configuring enviornment variables and application settings

* requirements.txt
    * This will list all the python packages needed for the project

* run.py
    * This is the entry point for running the Flask application

### APP
* The app/ directory contains the core application code

### API
* The api/ subdirectory houses the API endpoint, organised by version

* v1
    * reviews.py
    * users.py
    * places.py
    * ammenities.py

* __init__.py
    * This tells python to treat these directories as importable packages

### MODELS
* The models/ subdirectory contains the business logic classes
    * __init__.py
    * amenity.py
    * place.py
    * review.py
    * user.py

### PERSISTENCE
* The persistence/ subdirectory is where the in-memory repository is implemented. Later version will replace with a database using SQL Alchemy
    * __init__.py
    * repository.py

### SERVICES
* The services/ subdirectory is where the facade pattern is implemented. Managing the interaction between layers
    * __init__.py
    * facade.py

### TESTS
* The tests/ subdirectory contains the pytest tests for this project

### UTILS
* The utils/ subdirectory houses the custom errors
    * __init__.py
    * errors/
		* __init__.py
		* review_errors.py

# Authors
- Liani Mckeown
- Lachie King
- Uliana Deshin
- Anthonia Ifoeze
