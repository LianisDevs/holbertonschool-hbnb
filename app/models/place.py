from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place model"""
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        
        self.title = title
        self.description = description  
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    @property
    def title(self):
        """Get title value"""
        return self.__title
    
    @title.setter
    def title(self, value):
        """Set title value with validation"""
        if not value:
            raise ValueError("A title is required.")
        if not isinstance(value, str):
            raise TypeError("The title must be a string.")
        if len(value) > 100:
            raise ValueError("The title must not exceed 100 characters.")
        self.__title = value

    @property
    def description(self):
        """Get description value"""
        return self.__description
    
    @description.setter 
    def description(self, value):
        """Set description value with validation"""
        if value is not None and not isinstance(value, str):
            raise TypeError("The description must be a string.")
        self.__description = value

    @property
    def price(self):
        """Get price value"""
        return self.__price
    
    @price.setter
    def price(self, value):
        """Set price value with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("The price must be a number")
        if value <= 0:
            raise ValueError("The price must be a positive value.")
        self.__price = float(value)

    @property
    def latitude(self):
        """Get latitude value"""
        return self.__latitude
    
    @latitude.setter
    def latitude(self, value):
        """Set latitude value with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number.")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        self.__latitude = float(value)

    @property
    def longitude(self):
        """Get longitude value"""
        return self.__longitude
    
    @longitude.setter
    def longitude(self, value):
        """Set longitude value with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number.")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        self.__longitude = float(value)

    @property
    def owner(self):
        """Get owner value"""
        return self.__owner
    
    @owner.setter
    def owner(self, value):
        """Is this how you would validate user?? help pls"""

        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError("Owner must be an existing user.")
        self.__owner = value
