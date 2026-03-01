from app.models.review import Review
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.user import User
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        #register user
        user = User(user_data['first_name'], user_data['last_name'], user_data['email'], user_data['is_admin'])
        self.user_repo.add(user)
        return user

    def delete_user(self, user_id):
        pass

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user is None:
            return None
        
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)
        user.is_admin = user_data.get("is_admin", user.is_admin)
        return user

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if user is None:
            return None
        return user

    def get_user_by_email(self, email):
        user_email = self.user_repo.get_by_attribute('email', email)
        if user_email is None:
            return None
        return user_email

    def get_all_users(self):
        all_users = self.user_repo.get_all()
        if all_users is None:
            return []
        return all_users

    def create_place(self, owner_id, place_data):
        """Create a new place"""
        # Check if user id is in database
        user = self.user_repo.get(owner_id)
        if user is None:
            return None
        #create place instance
        place = Place(place_data["title"], place_data["price"], place_data["latitude"], place_data["longitude"], user.id)
       
       # Add place to repository
        self.place_repo.add(place)

        return place
    
    
    def update_place(self, place_id, place_data):
        """Update a place with new data"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    def delete_place(self, place_id):
        """Delete a place by ID"""
        place = self.place_repo.get(place_id)
        if not place:
            return False
        self.place_repo.delete(place_id)
        return True

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def get_place(self, place_id):
        """Get a specific place by ID"""
        return self.place_repo.get(place_id)

    def create_review(self, user_id, place_id, review_data):
        #check if user id is in database
        user = self.user_repo.get(user_id)
        if user is None:
            return None
        #check if place id is in database
        place = self.place_repo.get(place_id)
        if place is None:
            return None
        review = Review(review_data["text"], review_data["rating"], place.id, user.id)
        return review


    def update_review(self, review_id, review_data):
        pass

    def delete_review(self, review_id):
        pass

    def list_review(self, place_id):
        pass

    def create_amenity(self, amenity_data):
        amenity = Amenity(amenity_data["name"])
        # add amenity to local storage
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        
        return amenity        

    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        self.amenity_repo.delete(amenity_id)

        return amenity
