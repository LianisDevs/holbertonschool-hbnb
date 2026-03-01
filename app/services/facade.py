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
        """validates user and place and creates new review"""
        #check if user id is in database
        user = self.user_repo.get(user_id)
        if user is None:
            return None

        #check if place id is in database
        place = self.place_repo.get(place_id)
        if place is None:
            return None

        review = Review(review_data["text"], review_data["rating"], place.id, user.id)
        self.review_repo.add(review)
        return review


    def get_review(self, review_id):
        """Fetches review, returns None if no matching review"""
        review = self.review_repo.get(review_id)
        if review is None:
            return None
        return review


    def get_all_reviews(self):
        """Fetches all reviews, returns None if no reviews or list of reviews"""

        reviews = self.review_repo.get_all()
        if reviews is None:
            return []
        return reviews


    def get_reviews_by_place(self, place_id):
        """
        Fetches all reviews and filters by place_id
        Returns empty list if no reviews or list of reviews
        """
        reviews = self.review_repo.get_all()
        place_reviews = []
        for val in reviews:
            if val.place_id == place_id:
                place_reviews.append(val)
        return place_reviews


    def update_review(self, review_id, review_data):
        """
        Fetches review- if no review returns None
        Iterates through review_data, returns None if new keys are in review_data
        Returns updated_review
        """

        review = self.get_review(review_id)
        if review is None:
            return None

        for key in review_data.keys():
            if key not in dir(review):
                return None

        self.review_repo.update(review_id, review_data)

        updated_review = self.get_review(review_id)

        return updated_review


    def delete_review(self, review_id):
        """
        Fetches review- if no review returns None
        Deletes review
        """
        review = self.get_review(review_id)
        if review is None:
            return None

        self.review_repo.delete(review_id)


    def create_amenity(self, amenity_data):
        amenity = Amenity(amenity_data["name"])
        return amenity

    def update_amenity(self, amenity_id):
        pass

    def delete_amenity(self, amenity_id):
        pass

    def list_amenity(self, amenity_id):
        pass
