import pytest
from app.models.user import User
from app.models.place import Place
from app.services import facade
from app.services.facade import HBnBFacade
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from app.utils.errors.review_errors import ReviewInvalidDataError, ReviewNotFoundError

class TestReviewClass():
    facade = HBnBFacade()
    user = User('john', 'smith', 'js@gmail.com', False)
    place = Place('House on a hill', 500, 37.7749, -122.4194, user)
    place2 = Place('House on a haunted hill', 5003, 37.77349, -122.41194, user)

    def test_create_review(self):
        """
        Test: create_review(
        review is a Review class
        Correct attributes
        Values passed are on this instance
        """
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
        assert hasattr(review, "id")


    def test_create_review_text_not_string(self):
        review_data = {
            "text": 5,
            "rating": 5
        }
        with pytest.raises(TypeError):
            self.facade.create_review(self.user.id, self.place.id, review_data)


    def test_create_review_text_empty_string(self):
        review_data = {
            "text": "",
            "rating": 5
        }
        with pytest.raises(ValueError):
            self.facade.create_review(self.user.id, self.place.id, review_data)


    def test_create_review_text_over_1000_chars(self):
        review_data = {
            "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Na",
            "rating": 7
        }
        with pytest.raises(ValueError):
            self.facade.create_review(self.user.id, self.place.id, review_data)


    def test_create_review_rating_not_int(self):
        review_data = {
            "text": "Fab stay",
            "rating": "So nice"
        }
        with pytest.raises(TypeError):
            self.facade.create_review(self.user.id, self.place.id, review_data)


    def test_create_review_rating_not_between_1_and_5(self):
        review_data = {
            "text": "Fab stay",
            "rating": 7
        }
        with pytest.raises(ValueError):
            self.facade.create_review(self.user.id, self.place.id, review_data)


