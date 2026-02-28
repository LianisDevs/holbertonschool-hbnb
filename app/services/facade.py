from app.models.review import Review
from app.models.place import Place
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def register_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    def delete_user(self, user_id):
        pass

    def update_user(self, user_id):
        pass

    def get_user(self, user_id):
        pass

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
        """Create a new amenity: TEMPORARY ONLY FOR ULIANA TESTING, PLEASE CHANGE THIS LACHIE"""
        amenity = Amenity(amenity_data["name"])
        self.amenity_repo.add(amenity)
        return amenity

    def update_amenity(self, amenity_id):
        pass

    def delete_amenity(self, amenity_id):
        pass

    def list_amenity(self, amenity_id):
        pass
