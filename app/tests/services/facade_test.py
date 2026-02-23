import pytest

from app.models.user import User
from app.models.place import Place
from app.services.facade import HBnBFacade
from app.models.review import Review

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
