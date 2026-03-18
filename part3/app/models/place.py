from part3.app.models.base_model import BaseModel
from part3.app import db
from sqlalchemy import Float, Integer, Numeric, String
from sqlalchemy.orm import validates


class Place(BaseModel):
    """Place model"""
    __tablename__ = 'places'

    # Need amenities relationship to be mapped
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    owner_id = db.Column(db.String(36))
    price = db.Column(Float(), nullable=False)
    latitude = db.Column(String(20), nullable=False)
    longitude = db.Column(String(20), nullable=False)

    def __init__(self, title, price, latitude, longitude, owner_id, description=None, amenities=[]):
        super().__init__()

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    @validates("title")
    def validates_title(self, key, value):
        """Set title value with validation"""
        if not value:
            raise ValueError("A title is required.")

        if not isinstance(value, str):
            raise TypeError("The title must be a string.")

        if len(value) > 100:
            raise ValueError("The title must not exceed 100 characters.")

        return value

    @validates("description")
    def validates_description(self, key, value):
        """Set description value with validation"""
        if value is not None and not isinstance(value, str):
            raise TypeError("The description must be a string.")

        return value

    @validates("price")
    def validates_price(self, key, value):
        """Set price value with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("The price must be a number")

        if value < 0:
            raise ValueError("The price must be a positive value.")

        return float(value)

    @validates("latitude")
    def validates_latitude(self, key, value):
        """Set latitude value with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number.")

        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")

        return str(value)

    @validates("longitude")
    def validates_longitude(self, key, value):
        """Set longitude value with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number.")

        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")

        return str(value)

    @validates("owner_id")
    def validates_owner(self, key, value):
        """Set user as owner """
        return value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
