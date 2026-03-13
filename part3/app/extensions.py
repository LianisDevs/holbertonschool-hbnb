from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


# initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()