from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
