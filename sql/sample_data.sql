-- Insert required initial data for HBnB database

-- Insert Administrator User
INSERT INTO user (id, first_name, last_name, email, password, is_admin) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$j0nRt2jn6H6hIEYbtnpfzeOEwjYE786EzuQVGShO33r7xfmLqvU2C', TRUE);

-- Insert Amenities
INSERT INTO amenity (id, name) VALUES
('02743f6c-dbaf-47ae-9de8-71fbeb71cb26', 'WiFi'),
('df64cb5f-1770-4986-9530-ef2c0cfe2e93', 'Swimming Pool'),
('1ed46586-ddc6-4f7c-8c51-417591b1368d', 'Air Conditioning');