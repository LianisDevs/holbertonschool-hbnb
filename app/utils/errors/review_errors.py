

class ReviewNotFoundError(Exception):
     def __init__(self, message="Review not found"):
        self.message = message
        super().__init__(self.message)

class ReviewInvalidDataError(Exception):
     def __init__(self, message="Review data invalid"):
        self.message = message
        super().__init__(self.message)
