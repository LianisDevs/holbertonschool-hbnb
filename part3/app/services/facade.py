from part3.app.models.review import Review
from part3.app.models.place import Place
from part3.app.models.amenity import Amenity
from part3.app.models.user import User
from part3.app.persistence.class_repos.AmenityRepository import AmenityRepository
from part3.app.persistence.class_repos.ReviewRepository import ReviewRepository
from part3.app.persistence.class_repos.UserRepository import UserRepository
from part3.app.persistence.class_repos.PlaceRepository import PlaceRepository
from part3.app.persistence.repository import SQLAlchemyRepository
from part3.app.utils.errors.place_errors import PlaceNotFoundError
from part3.app.utils.errors.review_errors import ReviewAlreadyExistsError, ReviewInvalidDataError, ReviewNotFoundError
from part3.app.utils.errors.user_errors import UserNotFoundError


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

        # self.setup_admin()

    def setup_admin(self):
        """Create an admin for testing"""
        admin_data = {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@hbnb.com",
            "password": "password123"
        }

        # Check if they already exist to avoid errors on restart
        # Will need to be removed after testing/before launch!
        if not self.get_user_by_email(admin_data['email']):
            # Create admin account
            admin = self.create_user(admin_data)
            # set the is_admin flag to True
            admin.is_admin = True
            print(f"Admin user created: {admin.email} (ID: {admin.id})")

    # Placeholder method for creating a user

    def create_user(self, user_data):
        # register user
        user = User(**user_data)
        self.user_repo.add(user)

        return user

    def delete_user(self, user_id):
        self.user_repo.delete(user_id)

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
        user = self.get_user(user_id)

        return user

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)

        if user is None:
            return None

        return user

    def get_user_by_email(self, email):
        user_email = self.user_repo.get_user_by_email(email)

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

        # create place
        place = Place(**place_data)
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
        """validates user and place and creates new review"""
        # check if user id is in database
        user = self.user_repo.get(user_id)

        if user is None:
            raise UserNotFoundError

        # check if place id is in database
        place = self.place_repo.get(place_id)

        if place is None:
            raise PlaceNotFoundError

        # get all reviews
        reviews = self.review_repo.get_all()

        # filter through the list of reviews, append reviews to place_reviews list
        for val in reviews:
            if val.place_id == place_id and val.user_id == user_id:
                raise ReviewAlreadyExistsError

        review = Review(review_data["text"],
                        review_data["rating"], place.id, user.id)
        # Add review to database
        self.review_repo.add(review)

        return review

    def get_review(self, review_id):
        """Fetches review, returns None if no matching review"""
        review = self.review_repo.get(review_id)

        if review is None:
            raise ReviewNotFoundError

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
        # get all reviews
        reviews = self.review_repo.get_all()
        place_reviews = []

        # filter through the list of reviews, append reviews to place_reviews list
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
            raise ReviewNotFoundError

        for key in review_data.keys():
            if key not in dir(review):
                raise ReviewInvalidDataError

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
            raise ReviewNotFoundError

        self.review_repo.delete(review_id)

    def create_amenity(self, amenity_data):
        if not amenity_data.get("name"):
            return None
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

        if "name" in amenity_data:
            if not amenity_data["name"] or not amenity_data["name"].strip():
                return None
    
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)

    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return False

        self.amenity_repo.delete(amenity_id)
        return True


facade = HBnBFacade()
