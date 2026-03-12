import pytest
from app.models.place import Place
from app.models.user import User
from app.services.facade import HBnBFacade


class TestPlaceModel:
    def setup_method(self):
        self.facade = HBnBFacade()
        self.user = User('John', 'Doe', 'john@example.com', False)
        self.facade.user_repo.add(self.user)

#### Test 1: Place Creation with Valid Data

    def test_create_place_valid_data(self):
        place_data = {
            "title": "Test Treehouse",
            "description": "A beautiful test treehouse",
            "price": 200.00,
            "latitude": 36.7749,
            "longitude": -119.4194
        }
        place = self.facade.create_place(self.user.id, place_data)

        assert place is not None
        assert isinstance(place, Place)
        assert place.title == "Test Treehouse"
        assert place.description == "A beautiful test treehouse"
        assert place.price == 200.00
        assert place.latitude == 36.7749
        assert place.longitude == -119.4194
        assert place.owner == self.user.id

#### Test 2: Place Creation with Invalid Owner

    def test_create_place_invalid_owner(self):
        place_data = {
        "title": "Test Treehouse",
        "price": 150.00,
        "latitude": 40.7128,
        "longitude": -74.0060
    }
        place = self.facade.create_place("invalid_user_id", place_data)

        assert place is None

#### Test 3: Title Validation - Required Field

    def test_place_title_required(self):
        with pytest.raises(ValueError, match="A title is required"):
            place = Place("", 100.00, 40.7128, -74.0060, self.user)


#### Test 4: Title Validation - String Type

    def test_place_title_must_be_string(self):
        with pytest.raises(TypeError, match="The title must be a string"):
            place = Place(123, 100.00, 40.7128, -74.0060, self.user)


#### Test 5: Title Validation - Length Limit

    def test_place_title_length_limit(self):
        long_title = "x" * 101
        with pytest.raises(ValueError, match="The title must not exceed 100 characters"):
            place = Place(long_title, 100.00, 40.7128, -74.0060, self.user)


#### Test 6: Price Validation - Positive Value

    def test_place_price_positive(self):
        with pytest.raises(ValueError, match="The price must be a positive value"):
            place = Place("Valid Title", -100.00, 40.7128, -74.0060, self.user)

#### Test 7: Price Validation - Number Type

    def test_place_price_must_be_number(self):
        with pytest.raises(TypeError, match="The price must be a number"):
            place = Place("Valid Title", "invalid_price", 40.7128, -74.0060, self.user)

#### Test 8: Latitude Validation - Range

    def test_place_latitude_range(self):
        with pytest.raises(ValueError, match="Latitude must be between -90.0 and 90.0"):
            place = Place("Valid Title", 100.00, 95.0, -74.0060, self.user)

        with pytest.raises(ValueError, match="Latitude must be between -90.0 and 90.0"):
            place = Place("Valid Title", 100.00, -95.0, -74.0060, self.user)

#### Test 9: Longitude Validation - Range

    def test_place_longitude_range(self):
        with pytest.raises(ValueError, match="Longitude must be between -180.0 and 180.0"):
            place = Place("Valid Title", 100.00, 40.7128, 185.0, self.user)

        with pytest.raises(ValueError, match="Longitude must be between -180.0 and 180.0"):
            place = Place("Valid Title", 100.00, 40.7128, -185.0, self.user)

#### Test 10: Description Validation - Optional Field

    def test_place_description_optional(self):
        # Test with None description
        place = Place("Valid Title", 100.00, 40.7128, -74.0060, self.user, None)
        assert place.description is None

        # Test with valid string description
        place = Place("Valid Title", 100.00, 40.7128, -74.0060, self.user, "Valid description")
        assert place.description == "Valid description"


#### Test 11: Description Type Validation

    def test_place_description_type(self):
        with pytest.raises(TypeError, match="The description must be a string"):
            place = Place("Valid Title", 100.00, 40.7128, -74.0060, self.user, 123)


#### Test 12: Add Review Functionality

    def test_add_review_to_place(self):
        place = Place("Test House", 100.00, 40.7128, -74.0060, self.user)
        from app.models.review import Review
        review = Review("awesome place yayyyay!", 5, place.id, self.user.id)

        place.add_review(review)
        assert len(place.reviews) == 1
        assert place.reviews[0] == review


#### Test 13: Add Amenity Functionality

    def test_add_amenity_to_place(self):
        place = Place("Test House", 100.00, 40.7128, -74.0060, self.user)
        from app.models.amenity import Amenity
        amenity = Amenity("WiFi")

        place.add_amenity(amenity)
        assert len(place.amenities) == 1
        assert place.amenities[0] == amenity


#### Test 14: BaseModel Inheritance

    def test_place_inherits_basemodel_properties(self):
        place = Place("Test House", 100.00, 40.7128, -74.0060, self.user)

        assert hasattr(place, 'id')
        assert hasattr(place, 'created_at')
        assert hasattr(place, 'updated_at')
        assert isinstance(place.id, str)
        assert place.created_at is not None
        assert place.updated_at is not None