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

    def create_place(self, user_id, place_data):
        #check if user id is in database
        user = self.user_repo.get(user_id)
        if user is None:
            return None
        #create place instance
        place = Place(place_data["title"], place_data["price"], place_data["latitude"], place_data["longitude"], user.id)
        return place
    
    def update_place(self, place_id):
        pass

    def delete_place(self, place_id):
        pass

    def get_place(self, place_id):
        pass

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
