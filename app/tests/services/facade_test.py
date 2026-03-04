import pytest

from app.models.user import User
from app.models.place import Place
from app.services import facade
from app.services.facade import HBnBFacade
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from app.services.facade import HBnBFacade

class TestReviewClass():
    facade = HBnBFacade()
    user = User('john', 'smith', 'js@gmail.com', False)
    place = Place('House on a hill', 500, 37.7749, -122.4194, user)
    place2 = Place('House on a haunted hill', 5003, 37.77349, -122.41194, user)
    place3 = Place('Shack', 25, 27.77349, -42.41194, user)


    def test_create_review(self):
        """
        Test: create_review()
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


    def test_create_review_if_user_is_not_valid(self):
        """
        Test: create_review()
        If user is not valid- return None
        """
        review_data = {
            "text": "meh",
            "rating": 3
        }
        review = self.facade.create_review(2, self.place.id, review_data)
        assert review == None


    def test_create_review_if_place_is_not_valid(self):
        """
        Test: create_review()
        If place is not valid- return None
        """
        review_data = {
            "text": "meh",
            "rating": 3
        }
        review = self.facade.create_review(self.user.id, 4, review_data)
        assert review == None


    def test_get_review(self):
        """
        Test: get_review()
        Creates new review then tests you can fetch this review by id
        """
        review_data = {
            "text": "Horrible stay!",
            "rating": 1
        }
        review = self.facade.create_review(self.user.id, self.place.id, review_data)
        fetched_review = self.facade.get_review(review.id)
        assert fetched_review.id == review.id


    def test_get_review_if_review_is_not_valid(self):
        """
        Test: get_review()
        If review is not valid- return None
        """
        review = self.facade.get_review(1)
        assert review == None


    def test_get_all_reviews(self):
        """
        Test: get_all_reviews()
        Creates new empty facade, adds user, place and 3 reviews
        Checks all 3 reviews just added are returned in list
        """
        empty_facade = HBnBFacade()
        empty_facade.user_repo.add(self.user)
        empty_facade.place_repo.add(self.place)

        review_data_1 = {
            "text": "This was an amazing stay OMG",
            "rating": 5
        }
        review_data_2 = {
            "text": "Horrible stay!",
            "rating": 1
        }
        review_data_3 = {
            "text": "Horrible bad bad stay!",
            "rating": 1
        }
        empty_facade.place_repo.add(self.place2)

        review_1 = empty_facade.create_review(self.user.id, self.place.id, review_data_1)
        review_2 = empty_facade.create_review(self.user.id, self.place.id, review_data_2)
        review_3 = empty_facade.create_review(self.user.id, self.place2.id, review_data_3)

        reviews = empty_facade.get_all_reviews()
        assert review_1 in reviews
        assert review_2 in reviews
        assert review_3 in reviews


    def test_get_all_reviews_if_no_reviews(self):
        """
        Test: get_all_reviews()
        Creates new empty facade, adds user and place
        If no reviews in database- return empty list
        """
        empty_facade = HBnBFacade()
        reviews = empty_facade.get_all_reviews()
        assert reviews == []


    def test_get_reviews_by_place(self):
        """
        Test: get_reviews_by_place()
        Creates 3 reviews, 2 have place id 1 has place2 id
        Checks that reviews returned for place is review_1 and review_2
        """
        review_data_1 = {
            "text": "This was an amazing stay OMG",
            "rating": 5
        }
        review_data_2 = {
            "text": "Horrible stay!",
            "rating": 1
        }
        review_data_3 = {
            "text": "Horrible bad stay!",
            "rating": 1
        }

        review_1 = self.facade.create_review(self.user.id, self.place.id, review_data_1)
        review_2 = self.facade.create_review(self.user.id, self.place.id, review_data_2)
        review_3 = self.facade.create_review(self.user.id, self.place2.id, review_data_3)

        reviews = self.facade.get_reviews_by_place(self.place.id)
        assert review_1 in reviews
        assert review_2 in reviews
        assert review_3 not in reviews


    def test_get_reviews_by_place_if_place_has_no_reviews(self):
        """
        Test: get_reviews_by_place()
        Creates new place, this place has no reviews
        If no reviews with this place id- return empty list
        """
        # place with no reviews should retunr an empty array 
        self.facade.place_repo.add(self.place3)
        reviews = self.facade.get_reviews_by_place(self.place3.id)
        assert reviews == []


    def test_update_review(self):
        """
        Test: update_review()
        Creates new review
        Updates data on this review
        Asserts that data is now updated values
        """

        review_data = {
            "text": "What a view",
            "rating": 5
        }
        review = self.facade.create_review(self.user.id, self.place.id, review_data)

        new_review_data = {
            "text": "Bad smell",
            "rating": 4
        }
        updated_review = self.facade.update_review(review.id, new_review_data)

        assert updated_review.text == "Bad smell"
        assert updated_review.rating == 4


    def test_update_review_if_review_is_not_valid(self):
        """
        Test: update_review()
        If review id is not valid- returns None
        """
        review_data = {
            "text": "Slept good",
            "rating": 5
        }
        review = self.facade.update_review(2, review_data)
        assert review == None


    def test_update_review_if_review_data_is_not_valid(self):
        """
        Test: update_review()
        If review id is not valid- returns None
        """
        review_data = {
            "text": "What a view",
            "rating": 5
        }
        review = self.facade.create_review(self.user.id, self.place.id, review_data)

        updated_review_data = {
            "abc": 5
        }
        review = self.facade.update_review(review.id, updated_review_data)
        assert review == None


    def test_delete_review(self):
        """
        Test: delete_review()
        Creates new review
        Deletes this review
        Tries to get this review- return None
        """
        review_data = {
            "text": "What a view",
            "rating": 5
        }
        review = self.facade.create_review(self.user.id, self.place.id, review_data)
        self.facade.delete_review(review.id)
        deleted_review = self.facade.get_review(review.id)
        assert deleted_review == None

    def test_delete_review_if_review_is_not_valid(self):
        self.facade.delete_review(1)
        deleted_review = self.facade.get_review(1)
        assert deleted_review == None
class TestUserClass():
    facade = HBnBFacade()

    def test_create_user(self):
        user_data = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "js@gmail.com",
            "is_admin": False
        }
        user = self.facade.create_user(user_data)
        assert isinstance(user, User)
        assert user.first_name == "John"
        assert user.last_name == "Smith"
        assert user.email  == "js@gmail.com"
        assert user.is_admin == False
    
    def test_email_already_registered(self):
        user_data = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "js@gmail.com",
            "is_admin": False
        }
        self.facade.create_user(user_data)
        existing_user = self.facade.get_user_by_email("js@gmail.com")
        assert existing_user is not None
        
    def test_update_user(self):
        user_data = {
            "first_name": "Old",
            "last_name": "Name",
            "email": "oldname@gmail.com",
            "is_admin": False
        }
        user = self.facade.create_user(user_data)
        update_data = {
            "first_name": "New",
            "last_name": "Name",
            "email": "newname@gmail.com",
            "is_admin": False
        }
        updated_user = self.facade.update_user(user.id, update_data)
        assert updated_user is not None
        assert updated_user.first_name == "New"
        assert updated_user.email == "newname@gmail.com"
        
    def test_update_user_not_found(self):
        update_data = {
            "first_name": "Ghost",
            "last_name": "User",
            "email": "ghost@gmail.com",
            "is_admin": False
        }
        result = self.facade.update_user("nonexistent", update_data)
        assert result is None
        
    def test_get_user_by_id_found(self):
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@gmail.com",
            "is_admin": False
        }
        user = self.facade.create_user(user_data)
        found_user = self.facade.get_user(user.id)
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.first_name == "Jane"
        assert found_user.email == "jane@gmail.com"
        
    def test_get_user_by_id_not_found(self):
        user = self.facade.get_user("nonexistent-id")
        assert user is None
        
    def test_get_user_by_email_found(self):
        user_data = {
            "first_name": "Sam",
            "last_name": "Adams",
            "email": "sam@gmail.com",
            "is_admin": False
        }
        self.facade.create_user(user_data)
        found_user = self.facade.get_user_by_email("sam@gmail.com")
        assert found_user is not None
        assert found_user.email == "sam@gmail.com"
        assert found_user.first_name == "Sam"
    
    def test_get_user_by_email_not_found(self):
        user = self.facade.get_user_by_email("ghost@nowhere.com")
        assert user is None

    def test_retrieve_list_of_all_users(self):
        user_data_1 = {
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice@gmail.com",
            "is_admin": False
        }
        user_data_2 = {
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "bob@gmail.com",
            "is_admin": False
        }
        self.facade.create_user(user_data_1)
        self.facade.create_user(user_data_2)
        all_users = self.facade.get_all_users()
        assert isinstance(all_users, list)
        assert len(all_users) >= 2
        assert all(isinstance(u, User) for u in all_users)


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

    def test_get_amenity(self):
        # clear the amenity_repo before starting new test
        self.facade = HBnBFacade()
        self.facade.amenity_repo = InMemoryRepository()

        amenity_1 = self.facade.create_amenity({"name": "Pool"})
        amenity_2 = self.facade.create_amenity({"name": "Wi-Fi"})
        amenity_3 = self.facade.create_amenity({"name": "Air Conditioning"})

        amenity = self.facade.get_amenity(amenity_1.id)

        assert isinstance(amenity, Amenity)
        assert amenity.name == "Pool"

    def test_get_all_amenities(self):
        # clear the amenity_repo before starting new test
        self.facade = HBnBFacade()
        self.facade.amenity_repo = InMemoryRepository()

        amenity_1 = self.facade.create_amenity({"name": "Pool"})
        amenity_2 = self.facade.create_amenity({"name": "Wi-Fi"})
        amenity_3 = self.facade.create_amenity({"name": "Air Conditioning"})
        amenities = self.facade.get_all_amenities()

        assert isinstance(amenities, list)
        assert len(amenities) == 3
        assert any(amenity.name == "Pool" for amenity in amenities)

    def test_update_amenity(self):
        # clear the amenity_repo before starting new test
        self.facade = HBnBFacade()
        self.facade.amenity_repo = InMemoryRepository()

        amenity_1 = self.facade.create_amenity({"name": "Pool"})

        amenity = self.facade.update_amenity(amenity_1.id, {"name": "Swimming Pool"})

        assert isinstance(amenity, Amenity)
        assert amenity.name == "Swimming Pool"

    def test_delete_amenity(self):
        # clear the amenity_repo before starting new test
        self.facade = HBnBFacade()
        self.facade.amenity_repo = InMemoryRepository()

        amenity_1 = self.facade.create_amenity({"name": "Pool"})

        deleted = self.facade.delete_amenity(amenity_1.id)

        assert deleted is not None
        assert deleted.name == "Pool"

        assert self.facade.get_amenity(amenity_1.id) is None
