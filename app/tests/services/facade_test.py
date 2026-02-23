import pytest

from app.models.user import User
from app.models.place import Place
from app.services.facade import HBnBFacade
from app.models.review import Review
from app.models.amenity import Amenity

class TestReviewClass():
    facade = HBnBFacade()
    user = User('john', 'smith', 'js@gmail.com', False)
    place = Place('House on a hill', 500, 37.7749, -122.4194, user)

    def test_create_review(self):
        review_data = {
            "text": "This was an amazing stay OMG",
            "rating": 5
        }
        self.facade.user_repo.add(self.user)
        self.facade.place_repo.add(self.place)
        review = self.facade.create_review(self.user.id, self.place.id, review_data)
        assert isinstance(review, Review)
        assert review.text == "This was an amazing stay OMG"
        assert review.rating == 5
        assert review.user_id == self.user.id
        assert review.place_id == self.place.id

    def test_only_create_review_if_user_is_valid(self):
        review_data = {
            "text": "This was an amazing stay OMG",
            "rating": 5
        }
        review = self.facade.create_review(2, self.place.id, review_data)
        assert review == None

    def test_only_create_review_if_place_is_valid(self):
        review_data = {
            "text": "This was an amazing stay OMG",
            "rating": 5
        }
        review = self.facade.create_review(self.user.id, 4, review_data)
        assert review == None

class TestPlaceClass():
    facade = HBnBFacade()
    user = User('john', 'smith', 'js@gmail.com', False)

    def test_create_place(self):
        place_data = {
            "title": "Fantabulous Cottage in the Woods",
            "price": 50.00,
            "latitude": 37.7749,
            "longitude": -122.4194
        }
        self.facade.user_repo.add(self.user)
        place = self.facade.create_place(self.user.id, place_data)
        assert isinstance(place, Place)
        assert place.title == "Fantabulous Cottage in the Woods"
        assert place.price == 50.00
        assert place.latitude == 37.7749
        assert place.longitude == -122.4194

    def test_only_create_place_if_user_is_valid(self):
        place_data = {
            "title": "Fantabulous Cottage in the Woods",
            "price": 50.00,
            "latitude": 37.7749,
            "longitude": -122.4194
        }
        place = self.facade.create_place(2, place_data)
        assert place == None

class TestAmenity():
    facade = HBnBFacade()

    def test_create_amenity(self):
        amenity_data = {
            "name": "Swimming Pool for the ages"
        }
        amenity = self.facade.create_amenity(amenity_data)
        assert isinstance(amenity, Amenity)
        assert amenity.name == "Swimming Pool for the ages"