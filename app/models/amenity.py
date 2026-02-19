from base_model import BaseModel


class Amenity(BaseModel):
    """Amenity Class Model"""

    def __init__(self, name):
        super().__init__()
        self.name = name

    # getter for name
    @property
    def name(self):
        return self.__name

    # setter for name
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Amenity must have a name")
        if not isinstance(value, str):
            raise TypeError("Amenity must be a string")
        self.__name = value