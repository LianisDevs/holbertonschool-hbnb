from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from part3.app.models.base_model import BaseModel
from part3.app import db


class Review(BaseModel):
    """
    Review class

    Parameters: inherits BaseModel
    """
    
    text = db.Column(String(1000), nullable=False)
    rating = db.Column(Integer, nullable=False)
    # Foreign keys
    place_id = db.Column(String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @validates('text')
    def validates_text(self, key, value):
        if not value:
            raise ValueError("Review text cannot be empty")

        elif not isinstance(value, str):
            raise TypeError("Review text must be a string")

        elif len(value) > 1000:
            raise ValueError("Review text length must be 1000 or less chars")

        return value

    @validates('rating')
    def validates_rating(self, key, value):
        if not value:
            raise ValueError("Review rating cannot be empty")

        elif not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("Review rating must be an integer")

        elif value < 1 or value > 5:
            raise ValueError("Review rating must be between 1-5")

        return value

    @validates('place_id')
    def validates_place_id(self, key, value):
        return value

    @validates('user_id')
    def validates_user_id(self, key, value):
        return value

    def to_json(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }

    def to_json_id_text_rating(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
        }
