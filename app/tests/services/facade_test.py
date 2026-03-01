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