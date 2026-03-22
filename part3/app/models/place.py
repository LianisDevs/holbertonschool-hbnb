from part3.app.models.base_model import BaseModel
from part3.app import db
from sqlalchemy import Float, Integer, Numeric, String
from sqlalchemy.orm import validates

# Many-to-many association table for Place <-> Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey(
        'places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey(
        'amenities.id'), primary_key=True)
)


class Place(BaseModel):
    """Place model"""
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(Float(), nullable=False)
    latitude = db.Column(String(20), nullable=False)
    longitude = db.Column(String(20), nullable=False)

    # FOREIGN KEY
    owner_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False)

    # owner = db.relationship('User', backref='places', lazy=True)
    # Use relationship() in both models to link them.

    # RELATIONSHIPS
    # One-to-many: Place has many Reviews
    reviews = db.relationship('Review', backref='place', lazy=True)
    # Many-to-many: Place <-> Amenity via association table
    amenities = db.relationship('Amenity', secondary=place_amenity,
                                lazy='subquery', backref=db.backref('places', lazy=True))

    def __init__(self, title, price, latitude, longitude, owner_id, amenities, description=None):
        super().__init__()

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities

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
