# SQL Scripts Test Results

**NOTE:** These tests were completed with the schema_sqlite.sql file to create the schema. The only difference between schema_sqlite.sql and the original schema.sql is the language used, as some syntax suitable for MySQL is unsuitable for SQLite. 

These are the two changes made to schema.sql to create schema_sqlite.sql:
- no ON UPDATE CURRENT_TIMESTAMP (not supported on SQLite)
- added line: PRAGMA foreign_keys = ON; (this enables foreign key constraints explicitly, whereas MySQL doesn't need to do this)

## Setup
```bash
# Create database and schema
sqlite3 test_manual.db < sql/schema_sqlite.sql

# Insert sample data
sqlite3 test_manual.db < sql/sample_data.sql

# Start interactive SQLite session
sqlite3 test_manual.db
```

## Schema Creation Tests
### Check that the five tables were created successfully (amenity, user, place, review, place_amenity):

```bash
.tables
```
RESPONSE:
```
amenity        place          place_amenity  review         user
```
### Check that foreign keys are established for Place: 
```sql
PRAGMA foreign_key_list(place);
```
RESPONSE:
```
0|0|user|owner_id|id|NO ACTION|CASCADE|NONE
```
### Check that foreign keys are established for Review:
```sql
PRAGMA foreign_key_list(review);
```
RESPONSE:
```
0|0|place|place_id|id|NO ACTION|CASCADE|NONE
1|0|user|user_id|id|NO ACTION|CASCADE|NONE
```
### Check that foreign keys are established for Place_Amenity:
```sql
PRAGMA foreign_key_list(place_amenity);
```
RESPONSE:
0|0|amenity|amenity_id|id|NO ACTION|CASCADE|NONE
1|0|place|place_id|id|NO ACTION|CASCADE|NONE

### Check that indexes exist:
```sql
.indexes
```
RESPONSE:
```
idx_place_amenity_amenity         sqlite_autoindex_amenity_2      
idx_place_amenity_place           sqlite_autoindex_place_1        
idx_place_owner                   sqlite_autoindex_place_amenity_1
idx_review_place                  sqlite_autoindex_review_1       
idx_review_user                   sqlite_autoindex_review_2       
idx_user_email                    sqlite_autoindex_user_1         
sqlite_autoindex_amenity_1        sqlite_autoindex_user_2
```
### Check that tables have correct data types and constraints:
- User
```sql
PRAGMA table_info(user);
```
RESPONSE:
```
0|id|CHAR(36)|0||1
1|first_name|VARCHAR(255)|1||0
2|last_name|VARCHAR(255)|1||0
3|email|VARCHAR(255)|1||0
4|password|VARCHAR(255)|1||0
5|is_admin|BOOLEAN|0|FALSE|0
6|created_at|TIMESTAMP|0|CURRENT_TIMESTAMP|0
7|updated_at|TIMESTAMP|0|CURRENT_TIMESTAMP|0
```
- Amenity
```sql
PRAGMA table_info(amenity);
```
RESPONSE:
```
0|id|CHAR(36)|0||1
1|name|VARCHAR(255)|1||0
2|created_at|TIMESTAMP|0|CURRENT_TIMESTAMP|0
3|updated_at|TIMESTAMP|0|CURRENT_TIMESTAMP|0
```
- Place
```sql
PRAGMA table_info(place);
```
RESPONSE:
```
0|id|CHAR(36)|0||1
1|title|VARCHAR(255)|1||0
2|description|TEXT|0||0
3|price|DECIMAL(10, 2)|1||0
4|latitude|FLOAT|0||0
5|longitude|FLOAT|0||0
6|owner_id|CHAR(36)|1||0
7|created_at|TIMESTAMP|0|CURRENT_TIMESTAMP|0
8|updated_at|TIMESTAMP|0|CURRENT_TIMESTAMP|0
```
- Review
```sql
PRAGMA table_info(review);
```
RESPONSE:
```
0|id|CHAR(36)|0||1
1|text|TEXT|1||0
2|rating|INTEGER|1||0
3|user_id|CHAR(36)|1||0
4|place_id|CHAR(36)|1||0
5|created_at|TIMESTAMP|0|CURRENT_TIMESTAMP|0
6|updated_at|TIMESTAMP|0|CURRENT_TIMESTAMP|0
```
- Place_Amenity
```sql
PRAGMA table_info(place_amenity);
```
RESPONSE:
```
0|place_id|CHAR(36)|1||1
1|amenity_id|CHAR(36)|1||2
```
### Summary:
- All 5 tables created successfully: user, amenity, place, review, place_amenity
- Foreign key relationships established
- Indexes exist (not specified by instructions, I added it based on advice)
- Table structures verified with correct data types and constraints

## Sample Data Insertion Tests
### Check that there is one user and three amenities:
```sql
SELECT 'users' as table_name, COUNT(*) as count FROM user
UNION ALL
SELECT 'amenities', COUNT(*) FROM amenity
UNION ALL  
SELECT 'places', COUNT(*) FROM place
UNION ALL
SELECT 'reviews', COUNT(*) FROM review;
```
RESPONSE:
```
users|1
amenities|3
places|0
reviews|0
```

### Check that there is an Admin user with the correct UUID (36c9050e-ddd3-4c3b-9731-9f487208bbc1):
```sql
SELECT * FROM user WHERE is_admin = 1;
```
RESPONSE:
```
36c9050e-ddd3-4c3b-9731-9f487208bbc1|Admin|HBnB|admin@hbnb.io|$2b$12$j0nRt2jn6H6hIEYbtnpfzeOEwjYE786EzuQVGShO33r7xfmLqvU2C|1|2026-03-20 04:50:11|2026-03-20 04:50:11
```
### Check that amenities are inserted with correct names and UUIDS:
```sql
SELECT * FROM amenity;
```
RESPONSE: 
```
02743f6c-dbaf-47ae-9de8-71fbeb71cb26|WiFi|2026-03-20 04:50:11|2026-03-20 04:50:11
df64cb5f-1770-4986-9530-ef2c0cfe2e93|Swimming Pool|2026-03-20 04:50:11|2026-03-20 04:50:11
1ed46586-ddc6-4f7c-8c51-417591b1368d|Air Conditioning|2026-03-20 04:50:11|2026-03-20 04:50:11
```
### Summary:
- Admin user inserted with correct UUID (36c9050e-ddd3-4c3b-9731-9f487208bbc1)
- Email: admin@hbnb.io with bcrypt hashed password
- Admin privileges set to TRUE
- 3 amenities inserted: WiFi, Swimming Pool, Air Conditioning
- All amenities assigned proper UUIDs

## CRUD Operation Tests

## INSERT Operations
### Insert a regular user:
```sql
INSERT INTO user (id, first_name, last_name, email, password, is_admin) 
VALUES ('user-123', 'John', 'Doe', 'john.doe@test.com', 'hashed_password_123', 0);
```

### Insert a place owned by admin:
```sql
INSERT INTO place (id, title, description, price, latitude, longitude, owner_id)
VALUES ('place-123', 'Test Beach House', 'Beautiful oceanfront property', 250.00, 37.7749, -122.4194, '36c9050e-ddd3-4c3b-9731-9f487208bbc1');
```

### Insert place-amenity relationships (many-to-many):
```sql
INSERT INTO place_amenity (place_id, amenity_id) VALUES ('place-123', '02743f6c-dbaf-47ae-9de8-71fbeb71cb26');
INSERT INTO place_amenity (place_id, amenity_id) VALUES ('place-123', 'df64cb5f-1770-4986-9530-ef2c0cfe2e93');
```

### Insert a review:
```sql
INSERT INTO review (id, text, rating, user_id, place_id)
VALUES ('review-123', 'Amazing place with great amenities!', 5, 'user-123', 'place-123');
```

## SELECT Operations
### Basic record retrieval:
```sql
SELECT COUNT(*) FROM user;
```
RESPONSE:
```
2
```

### Complex JOIN query:
```sql
SELECT p.title, p.price, a.name as amenity, r.rating, r.text
FROM place p
LEFT JOIN place_amenity pa ON p.id = pa.place_id
LEFT JOIN amenity a ON pa.amenity_id = a.id
LEFT JOIN review r ON p.id = r.place_id
WHERE p.id = 'place-123';
```
RESPONSE:
```
Test Beach House|250.0|WiFi|5|Amazing place with great amenities!
Test Beach House|250.0|Swimming Pool|5|Amazing place with great amenities!
```

## UPDATE Operations
### Update place price:
```sql
UPDATE place SET price = 300.00 WHERE id = 'place-123';
```

### Verify the update:
```sql
SELECT title, price FROM place WHERE id = 'place-123';
```
RESPONSE:
```
Test Beach House|300.0
```

## DELETE Operations
### Delete a review:
```sql
DELETE FROM review WHERE id = 'review-123';
```

### Verify deletion:
```sql
SELECT COUNT(*) FROM review WHERE id = 'review-123';
```
RESPONSE:
```
0
```

## Constraint Validation Tests
### Test duplicate email constraint (should fail):
```sql
INSERT INTO user (id, first_name, last_name, email, password, is_admin) 
VALUES ('test-123', 'Test', 'User', 'admin@hbnb.io', 'password123', 0);
```
RESPONSE:
```
Runtime error: UNIQUE constraint failed: user.email (19)
```

### Test check constraint on ratings (should fail for rating > 5):
```sql
INSERT INTO review (id, text, rating, user_id, place_id)
VALUES ('bad-review', 'Bad rating test', 6, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'place-123');
```
RESPONSE:
```
Runtime error: CHECK constraint failed: rating >= 1 AND rating <= 5 (19)
```

### Test unique review constraint (one review per user per place):
```sql
INSERT INTO review (id, text, rating, user_id, place_id)
VALUES ('duplicate-review', 'Duplicate review', 3, 'user-123', 'place-123');
```
RESPONSE:
```
Runtime error: UNIQUE constraint failed: review.user_id, review.place_id (19)
```

### Test foreign key constraint (should fail with non-existent user):
```sql
INSERT INTO place (id, title, description, price, latitude, longitude, owner_id)
VALUES ('fake-place', 'Test', 'Test place', 100.00, 0, 0, 'non-existent-user-id');
```
RESPONSE:
```
Runtime error: FOREIGN KEY constraint failed (19)
```

## Cleanup
```bash
# Remove test database
rm test_manual.db
```
