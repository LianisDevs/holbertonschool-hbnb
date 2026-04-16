# HBNB
This Repository contains the files for the HBNB project. HBNB replicates the basic functionalities of the AirBNB application, which allows users to find and book short term rentals. These users can also leave reviews on the locations they stay at.

### Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Admin Features](#admin-features)
  - [User](#user)
  - [Place](#place)
  - [Review](#review)
  - [Amenity](#amenity)
- [Tests](#tests)
- [Files](#files)
- [Authors](#authors)

# Features
CRUD capabilities for User/ Place/ Review/ Amenities with admin role-based access control 

# Requirements
This project requires Python version 3.14 or later. To check what version of Python you have installed use the command below:
```bash
python --version
```
# Installation
1. Clone the repository locally
```bash
git clone https://github.com/LianisDevs/holbertonschool-hbnb
```
2. Navigate to this directory
```bash
cd holbertonschool-hbnb
```
3. Install the dependencies using
```bash
pip install -r requirements.txt
```

# Usage
Run the application from the holbertonschool-hbnb directory
```bash
python3 run.py
```
Flask will provide the URL to run, such as 127.0.0.1:5000. Make sure to add /app to the end of the url for it to work.

Use tools like Postman or cURL to use the API endpoints, below examples use curl:

## Admin Features

This application includes admin functionality that allows administrators to bypass regular user limitations and perform elevated operations.

### Admin Account Setup

#### Elevate User to Admin
For testing, any authenticated user can elevate themselves to admin using the mock endpoint:

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/reviews/elevate_admin" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Expected Response:**
```jsonc
{
    "access_token": "new_jwt_token_with_admin_claims"
}

// 200 OK
```

**Note:** This endpoint is for testing only and should be removed in production.

#### Database-Level Admin Creation
In production, admin status should be set directly in the database by modifying the `is_admin` field in the user record.

### Admin Authentication

Admins receive JWT tokens with special claims that identify their elevated status:

```jsonc
{
  "identity": "user_id",
  "additional_claims": {
    "is_admin": true
  }
}
```

All admin operations are validated by checking these JWT claims on each request.

### Admin-Only Operations

#### Create Amenity (Admin Required)
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
  -d '{"name": "Swimming Pool"}'
```

**Expected Response (Admin):**
```jsonc
{
  "id": "amenity-id-123",
  "name": "Swimming Pool"
}

// 201 Created
```

**Expected Response (Non-Admin):**
```jsonc
{
  "error": "Unauthorized action"
}

// 403 Forbidden
```

#### Update Amenity (Admin Required)
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/amenities/amenity-id-123" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
  -d '{"name": "Olympic Swimming Pool"}'
```

#### Delete Amenity (Admin Required)
```bash
curl -X DELETE "http://127.0.0.1:5000/api/v1/amenities/amenity-id-123" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE"
```

### Admin Bypass Capabilities

#### Admin User Management
Admins can update or delete any user account:

```bash
# Update any user (admin can modify any user_id)
curl -X PUT "http://127.0.0.1:5000/api/v1/users/ANY_USER_ID_HERE" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "first_name": "Admin Updated Name"
  }'
```

#### Admin Place Management
Admins can create places for other users and manage any place:

```bash
# Admin creating a place for another user
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "title": "Admin Created Place",
    "price": 200.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "DIFFERENT_USER_ID_HERE",
    "amenities": ["amenity-id-123"]
  }'

# Admin updating any place
curl -X PUT "http://127.0.0.1:5000/api/v1/places/ANY_PLACE_ID_HERE" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "title": "Admin Updated Title"
  }'
```

#### Admin Review Management
Admins can modify or delete any user's reviews:

```bash
# Admin updating any review
curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/ANY_REVIEW_ID_HERE" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "text": "Admin moderated review",
    "rating": 3
  }'

# Admin deleting any review
curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/ANY_REVIEW_ID_HERE" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE"
```

### Security Notes

- Admin status is securely stored in JWT additional_claims
- Users cannot modify email or password
- All endpoints verify either ownership OR admin status
- Missing `is_admin` claims default to `false` for security


## User

#### Testing the Creation of a User
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "password": "ilikecats"
  }'
```

**Expected Response**

```jsonc
{
    "id": "b0fc1e80-e91d-43d0-bb4d-c686952adeff",
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com"
}

// 201 Created
```
#### Testing User Login 
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -H "Content-Type: application/json" -d '{
  "email": "john.doe@example.com",
  "password": "your_password"
}'
```

**Expected Response**

```jsonc
{
    "access_token": "your_generated_jwt_token"
}

// 200 ok
```

#### Testing User Authorization
```bash
curl -X GET "http://127.0.0.1:5000/api/v1/protected" -H "Authorization: Bearer your_generated_jwt_token"
```

**Expected Response**

```jsonc
{
    "message": "Hello, user 3fa85f64-5717-4562-b3fc-2c963f66afa6"
}

// 200 ok
```

#### Testing Email Already Registered
First create a user, then attempt to register again with the same email.

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com"
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
    "email": "john.smith@example.com"
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
    "email": "not-a-valid-email"
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
        "email": "john.smith@example.com"
    },
    {
        "id": "11c914d0-d55b-58e2-c1g3-990639b7b127",
        "first_name": "Alice",
        "last_name": "Wonder",
        "email": "alice.wonder@example.com"
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
    "email": "john.smith@example.com"
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
    "email": "john.smith@example.com"
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

### GET PLACES BY USER
Testing Get Places by User
Replace <user_id> with your own user ID and use your JWT token:
```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/YOUR_USER_ID_HERE/places"
```
**Expected Response**

```jsonc

  "places": [
    {
      "id": "38e80995-e208-4cdf-ac6a-359e1bcd52e1",
      "title": "Cozy Apartment",
      "description": "A nice place to stay",
      "price": 100.0,
      "latitude": "37.7749",
      "longitude": "-122.4194",
      "amenities": [
        "SHARKS"
      ],
      "reviews": [
        {
          "text": "Such a lovely stay!",
          "rating": 5
        }
      ],
      "created_at": "2026-03-22T06:35:28.380720",
      "updated_at": "2026-03-22T06:35:28.380725"
    }
  ]
}
```

### UPDATE USER

Updating user information requires JWT authentication. Users can only update their own information and cannot modify email or password fields.

#### Testing Update a User — Success

Replace <user_id> with your own user ID and use your JWT token:
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/YOUR_USER_ID_HERE" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "first_name": "Updated Name",
    "last_name": "Smith"
  }'
```

**Expected Response**

```jsonc
{
    "id": "00b803c9-c44a-47d1-b0f2-889528a6f016",
    "first_name": "Updated Name",
    "last_name": "Smith",
    "email": "john.smith@example.com"
}

// 200 OK
```

#### Testing Update User — Forbidden Fields
Attempting to modify email or password:
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/YOUR_USER_ID_HERE" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "first_name": "Updated Name",
    "email": "newemail@example.com",
    "password": "newpassword"
  }'
```

**Expected Response**

```jsonc
{
    "error": "You cannot modify email or password."
}

// 400 Bad Request
```

#### Testing Update User — Unauthorized
Attempting to update another user's information (Non-Admin):
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/SOMEONE_ELSES_USER_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "first_name": "Hacked Name"
  }'
```

**Expected Response (Non-Admin)**

```jsonc
{
    "error": "Unauthorized action."
}

// 403 Forbidden
```

#### Testing Update User — Admin Override
Admins can update any user's information:
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/ANY_USER_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "first_name": "Admin Updated Name"
  }'
```

**Expected Response (Admin)**

```jsonc
{
    "id": "user-id-123",
    "first_name": "Admin Updated Name", 
    "last_name": "Original LastName",
    "email": "user@example.com"
}

// 200 OK
```

#### Testing Update User — No Authentication
Attempting to update user information without JWT token:
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/YOUR_USER_ID_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "No Auth Update"
  }'
```

**Expected Response**

```jsonc
{
    "msg": "Missing Authorization Header"
}

// 401 Unauthorized
```

#### Testing Update a User — User Not Found
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/users/nonexistent-id-999" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "first_name": "Ghost",
    "last_name": "User"
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
curl -X PUT "http://127.0.0.1:5000/api/v1/users/YOUR_USER_ID_HERE" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
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
    "email": "john.smith@example.com"
}

// 200 OK
```
## Place
Before completing these tests, ensure you have a valid user UUID generated from creating a User (found in the User section). You will also need to create two distinct amenities with their own valid ids (create an amenity using instructions from the Amenity section).

To create a Place using the JSON format, you can use the below example. Fill in the required fields within acceptable ranges. 

Requirements: 
- Title must be a string equal to or below 100 chars
- Description is optional, and must be a string if added  
- Price must be a positive number
- Latitude must be between -90 and 90
- Longitude must be between -180 and 180
- Any amenities added must be valid (create amenities first using the Amenity section)

Prerequisites
Before completing these tests, ensure you have:
1. Created a user account (see User section)
2. Logged in to get a JWT token (see User Login section) 
3. Created at least one amenity (see Amenity section)

First, create a user and log in to get your JWT token:

```bash
# 1. Create a user
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "first_name": "Test",
    "last_name": "User", 
    "email": "testuser@example.com",
    "password": "password123"
  }'

# 2. Login to get JWT token
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "password123"
  }'

# 3. Create an amenity (needed for places)
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}'
```

# Testing Authenticated Place Creation
**Note:** The `owner_id` is automatically set from your JWT token and should NOT be included in the request body.

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "title": "Fantabulous Cottage in the Woods",
    "description": "A super cute cottage where you can live out your fairytale dreams!",
    "price": 250.00,
    "latitude": 36.7489,
    "longitude": -119.7722,
    "amenities": ["YOUR_AMENITY_ID_HERE"]
  }'
```

**Expected Response:**
```jsonc
{
  "id": "19d8e3bd-f3b2-4e82-97b6-2eae5324f176",
  "title": "Fantabulous Cottage in the Woods", 
  "description": "A super cute cottage where you can live out your fairytale dreams!",
  "price": 250.0,
  "latitude": 36.7489,
  "longitude": -119.7722,
  "owner_id": "7ddbcbe2-aed4-4fb4-a470-76077d1917bc",
  "amenities": ["da3d8ad9-ce41-4efc-9d0b-bf27d948e21a"],
  "reviews": [],
  "created_at": "2026-03-13T15:43:16.943669",
  "updated_at": "2026-03-13T15:43:16.943676"
}

// 201 Created
```

# Testing Unauthorized Place Creation
Attempting to create a place without authentication:

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Unauthorized Place",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "amenities": ["YOUR_AMENITY_ID_HERE"]
  }'
```

**Expected Response:**
```jsonc
{
  "msg": "Missing Authorization Header"
}

// 401 Unauthorized
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
  "reviews": [
  {
    "text": "Such a lovely stay!",
    "rating": 5
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
  "reviews": [
    {
      "text": "Such a lovely stay!",
      "rating": 5
    }
  ],
  "created_at": "2026-03-03T10:30:00.123456",
  "updated_at": "2026-03-03T10:30:00.123456"
}

// 200 OK
```
#### UPDATE PLACE
Only the owner of a place can update it. You must include the JWT token of the place owner.

Update an existing place with the fields that require change:
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/places/YOUR_PLACE_ID_HERE" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "title": "Updated Beach House",
    "description": "Newly renovated oceanfront property",
    "price": 300.00
  }'
```

**Expected Response:**
```jsonc
{
  "id": "19d8e3bd-f3b2-4e82-97b6-2eae5324f176",
  "title": "Updated Beach House",
  "description": "Newly renovated oceanfront property",
  "price": 300.0,
  "latitude": 36.7489,
  "longitude": -119.7722,
  "owner_id": "7ddbcbe2-aed4-4fb4-a470-76077d1917bc",
  "amenities": ["da3d8ad9-ce41-4efc-9d0b-bf27d948e21a"],
  "created_at": "2026-03-13T15:43:16.943669",
  "updated_at": "2026-03-13T15:44:13.444682"
}

// 200 OK
```

#### Testing Unauthorized Place Update
Attempting to update someone else's place with your JWT token (Non-Admin):

```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/places/SOMEONE_ELSES_PLACE_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "title": "Hacked Title"
  }'
```

**Expected Response (Non-Admin):**
```jsonc
{
  "error": "Unauthorized action"
}

// 403 Forbidden  
```

#### Testing Admin Place Update Override
Admins can update any place regardless of ownership:

```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/places/ANY_PLACE_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
  -d '{
    "title": "Admin Updated Place",
    "description": "Admin can update any place",
    "price": 350.00
  }'
```

**Expected Response (Admin):**
```jsonc
{
  "id": "place-id-123",
  "title": "Admin Updated Place",
  "description": "Admin can update any place",
  "price": 350.0,
  "latitude": 36.7489,
  "longitude": -119.7722,
  "owner_id": "original-owner-id",
  "amenities": ["amenity-id"],
  "created_at": "2026-03-13T15:43:16.943669",
  "updated_at": "2026-03-13T16:12:33.555888"
}

// 200 OK
```

#### Testing Place Update Without Authentication
Attempting to update a place without providing a JWT token:

```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/places/YOUR_PLACE_ID_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "No Auth Update"
  }'
```

**Expected Response:**
```jsonc
{
  "msg": "Missing Authorization Header"
}

// 401 Unauthorized
```
## Review

Creating, updating, and deleting reviews requires JWT authentication. The user_id is automatically set from the JWT token and should not be included in the request body.

#### CREATE A REVIEW
To create a review you need a valid place_id and JWT token. The user_id is automatically set from your authentication token:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     -d '{
    "text": "Dream stay, can't wait to go back!",
    "rating": 5,
    "place_id": "YOUR_PLACE_ID_HERE"
    }'
```
Expected response valid data:
```jsonc
{
  "id": "03bc36fd-fc43-4c51-a08b-eca82c5fe9fd",
  "text": "Great place to stay!",
  "rating": 5,
  "user_id": "df2e423b-9110-4c5c-b867-46f02c4640f9",
  "place_id": "19d8e3bd-f3b2-4e82-97b6-2eae5324f176"
}

// 201 Created
```

#### Testing Review Creation
Trying to review your own place:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer PLACE_OWNER_JWT_TOKEN" \
     -d '{
    "text": "Reviewing my own place",
    "rating": 5,
    "place_id": "YOUR_OWN_PLACE_ID"
    }'
```
Expected response:
```jsonc
{
  "error": "You cannot review your own place."
}

// 400 Bad Request
```

#### Testing Unauthorized Review Creation
Attempting to create a review without authentication:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
     -H "Content-Type: application/json" \
     -d '{
    "text": "Unauthorized review",
    "rating": 5,
    "place_id": "SOME_PLACE_ID"
    }'
```
Expected response:
```jsonc
{
  "msg": "Missing Authorization Header"
}

// 401 Unauthorized
```
#### UPDATE REVIEW
Only the review author can update their own review.

To update a review you need a valid review_id and JWT token from the review author:
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/YOUR_REVIEW_ID_HERE" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     -d '{
         "text": "Horrible stay", 
         "rating": 1
     }'
```
Expected response valid data:
```jsonc
{
  "message": "Review updated successfully"
}

// 200 OK
```

#### Testing Unauthorized Review Update
Attempting to update someone else's review (Non-Admin):
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/SOMEONE_ELSES_REVIEW_ID" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
     -d '{
         "text": "Hacked review"
     }'
```
Expected response (Non-Admin):
```jsonc
{
  "error": "Unauthorized action."
}

// 403 Forbidden
```

#### Testing Admin Review Update Override
Admins can update any review regardless of authorship:
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/ANY_REVIEW_ID" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
     -d '{
         "text": "Admin moderated this review",
         "rating": 3
     }'
```
Expected response (Admin):
```jsonc
{
  "message": "Review updated successfully"
}

// 200 OK
```

#### Testing Review Update Without Authentication
Attempting to update a review without JWT token:
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/SOME_REVIEW_ID" \
     -H "Content-Type: application/json" \
     -d '{
         "text": "No auth update"
     }'
```
Expected response:
```jsonc
{
  "msg": "Missing Authorization Header"
}

// 401 Unauthorized
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
Only the review author can delete their own review.

To delete a review you need a valid review_id and JWT token from the review author:
```bash
curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/YOUR_REVIEW_ID_HERE" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```
Expected response valid data:
```jsonc
{
  "message": "Review deleted successfully"
}

// 200 OK
```

#### Testing Unauthorized Review Deletion
Attempting to delete someone else's review (Non-Admin):
```bash
curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/SOMEONE_ELSES_REVIEW_ID" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```
Expected response (Non-Admin):
```jsonc
{
  "error": "Unauthorized action."
}

// 403 Forbidden
```

#### Testing Admin Review Deletion Override
Admins can delete any review regardless of authorship:
```bash
curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/ANY_REVIEW_ID" \
     -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE"
```
Expected response (Admin):
```jsonc
{
  "message": "Review deleted successfully"
}

// 200 OK
```

#### Testing Review Deletion Without Authentication
Attempting to delete a review without JWT token:
```bash
curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/SOME_REVIEW_ID"
```
Expected response:
```jsonc
{
  "msg": "Missing Authorization Header"
}

// 401 Unauthorized
```
## Amenity
**Note:** All amenity creation, updates, and deletion operations require admin privileges.

#### CREATE AMENITY (Admin Required)

To create an amenity, you must be authenticated as an admin. Use the JSON format below:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
     -d '{"name":"Swimming Pool"}'
```
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
     -d '{"name":"Fitness Center"}'
```

**Expected Output (Admin):**
```jsonc
{
  "id": "amenity-id-123",
  "name": "Swimming Pool"
}
```

**Expected Output (Non-Admin):**
```jsonc
{
  "error": "Unauthorized action"
}

// 403 Forbidden
```

#### Testing Amenity Creation Without Authentication
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Unauthorized Amenity"}'
```

**Expected Output:**
```jsonc
{
  "msg": "Missing Authorization Header"
}

// 401 Unauthorized
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

#### UPDATE AMENITY (Admin Required)

To update an amenity, you must be authenticated as an admin. Use the amenity ID in the URL:
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/AMENITY_ID_HERE \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE" \
-d '{"name": "Updated Amenity Name"}'
```

**Expected Output (Admin):**
```jsonc
{
  "id": "amenity-id-123",
  "name": "Updated Amenity Name"
}

// 200 OK
```

**Expected Output (Non-Admin):**
```jsonc
{
  "error": "Unauthorized action"
}

// 403 Forbidden
```

#### DELETE AMENITY (Admin Required)

To delete an amenity, you must be authenticated as an admin:
```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/amenities/YOUR_AMENITY_ID_HERE \
     -H "Authorization: Bearer ADMIN_JWT_TOKEN_HERE"
```

**Expected Output (Admin):**
```jsonc
{
  "message": "Amenity deleted successfully"
}

// 200 OK
```

**Expected Output (Non-Admin):**
```jsonc
{
  "error": "Unauthorized action"
}

// 403 Forbidden
```

If the amenity does not exist, the API will return:
```jsonc
{
  "error": "Amenity not found"
}
```

If the JWT token is missing or the user is not allowed to delete the amenity, the API will return an authentication or authorization error.

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
