from email_validator import validate_email, EmailNotValidError
from part3.app.models.base_model import BaseModel
from part3.app import db, bcrypt
from sqlalchemy.orm import validates

class User(BaseModel):
    """"User model"""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationship
    # One-to-many: User owns many Places
    places = db.relationship('Place', backref='owner', lazy=True)
    # One-to-many: User writes many Reviews
    reviews = db.relationship('Review', backref='author', lazy=True)



    def __init__(self, first_name, last_name, email, password):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


    """Validates first name"""
    @validates("first_name")
    def validates_first_name(self, key, value):
        if not value:
            raise ValueError("First Name is required")

        if len(value) > 50:
            raise ValueError(
            "First Name length must be "
            "less than or equal to 50 characters")

        if not isinstance(value, str):
            raise TypeError("First Name must be a string")

        return value
 

    """Validates last name"""
    @validates("last_name")
    def validates_last_name(self, key, value):
        if not value:
            raise ValueError("Last Name is required")

        if len(value) > 50:
            raise ValueError(
            "Last Name length must be "
            "less than or equal to 50 characters")

        if not isinstance(value, str):
            raise TypeError("Last Name must be a string")

        return value

 
    """Validates email"""
    @validates("email")
    def validates_email(self, key, value):
        try:
            email_info = validate_email(value, check_deliverability=False)
            normalized_email = email_info.normalized
            return normalized_email

        except EmailNotValidError:
            raise EmailNotValidError("User email must be a valid email address")
 

    """Validates admin"""
    @validates("is_admin")
    def validates_is_admin(self, key, value):
        if not isinstance(value, bool):
            print("issue with",value)
            print(isinstance(value, bool))
            raise TypeError("is_admin must be true or false")

        return value

    @validates("password")
    def validates_and_hashes_password(self, key, password):
        """Hashes the password before storing it."""
        if password is None:
            raise ValueError("Password cannot be None")

        return bcrypt.generate_password_hash(password).decode('utf-8')

 
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if not self.password:
            return False

        return bcrypt.check_password_hash(self.password, password)

