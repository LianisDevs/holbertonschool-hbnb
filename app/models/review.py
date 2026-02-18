from base_model import BaseModel

class Review(BaseModel):
    """
    Review class

    Parameters: inherits BaseModel
    """

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not value:
            raise ValueError("Review text cannot be empty")
        elif not isinstance(value, str):
            raise TypeError("Review text must be a string")
        elif len(value) > 1000:
            raise ValueError("Review text length must be 1000 or less chars")
        self.__text = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not value:
            raise ValueError("Review rating cannot be empty")
        elif not isinstance(value, int):
            raise TypeError("Review rating must be an integer")
        elif value < 1 or value > 5:
            raise ValueError("Review rating must be between 1-5")
        self.__rating = value

    @property
    def place_id(self):
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        self.__place_id = value

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        self.__user_id = value
