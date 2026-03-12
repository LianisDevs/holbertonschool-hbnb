

class PlaceNotFoundError(Exception):
     def __init__(self, message="Place not found"):
        self.message = message
        super().__init__(self.message)
