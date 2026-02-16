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
        pass

    def update_place(self, place_id):
        pass

    def delete_place(self, place_id):
        pass

    def get_place(self, place_id):
        pass

    def create_review(self, user_id, place_id, review_data):
        pass

    def update_review(self, review_id, review_data):
        pass

    def delete_review(self, review_id):
        pass

    def list_review(self, place_id):
        pass

    def create_amenity(self, amenity_data):
        pass

    def update_amenity(self, amenity_id):
        pass

    def delete_amenity(self, amenity_id):
        pass

    def list_amenity(self, amenity_id):
        pass
