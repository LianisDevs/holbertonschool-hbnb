from part3.app.models.base_model import BaseModel
from part3.app import db
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    """Amenity Class Model"""
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False)


    def __init__(self, name):
        super().__init__()
        self.name = name


    @validates("name")
    def validates_name(self, key, value):
        if not value:
            raise ValueError("Amenity must have a name")

        if not isinstance(value, str):
            raise TypeError("Amenity must be a string")

        if len(value) > 50:
            raise ValueError("Amenity name must be 50 characters\
             or less")

        return value
