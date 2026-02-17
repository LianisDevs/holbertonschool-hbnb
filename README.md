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


# AUTHORS
- Liani Mckeown
- Lachie King
- Uliana Deshin
- Anthonia Ifoeze
