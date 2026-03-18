from part3.app.models.amenity import Amenity
from part3.app import db
from part3.app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
