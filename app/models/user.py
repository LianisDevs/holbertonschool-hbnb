from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError

class User(BaseModel):
    """"User model"""
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    """Get Value for first name"""
    @property
    def first_name(self):
        return self.__first_name

    """Set values for first name"""
    @first_name.setter
    def first_name(self, value):
        if not value:
            raise ValueError("First Name is required")
        if len(value) > 50:
            raise ValueError(
            "First Name length must be "
            "less than or equal to 50 characters")
        if not isinstance(value, str):
            raise TypeError("First Name must be a string")
        self.__first_name = value
 
    """Get Value for last name"""
    @property
    def last_name(self):
        return self.__last_name

    """Set values for last name"""
    @last_name.setter
    def last_name(self, value):
        if not value:
            raise ValueError("Last Name is required")
        if len(value) > 50:
            raise ValueError(
            "Last Name length must be "
            "less than or equal to 50 characters")
        if not isinstance(value, str):
            raise TypeError("Last Name must be a string")
        self.__last_name = value

    """Get value for email"""
    @property
    def email(self):
        return self.__email
 
    """Set value for email"""
    @email.setter
    def email(self, value):
        try:
            email_info = validate_email(value, check_deliverability=False)
            self.__email = email_info
        except EmailNotValidError:
            raise EmailNotValidError("User email must be a valid email address")
 
    """Get value for admin"""
    @property
    def is_admin(self):
        return self.__is_admin
 
    """Set value for admin"""
    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            print("issue with",value)
            print(isinstance(value, bool))
            raise TypeError("is_admin must be true or false")
        self.__is_admin = value
