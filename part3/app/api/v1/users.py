from flask_restx import Namespace, Resource, fields
from part3.app.services import facade
from email_validator.exceptions import EmailNotValidError
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from part3.app.utils.errors.user_errors import UserNotFoundError

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
})

# Define the user update model (excludes email and password)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new user"""

        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except EmailNotValidError:
            return {'error': 'User email must be a valid email'}, 400

        return {'id': new_user.id, 'message': 'User created successfully'}, 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Retrieve list of all users"""

        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_admin': user.is_admin
            }
            for user in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_update_model, validate=False)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update a user"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        # Set is_admin default to False if not exists
        is_admin = claims.get('is_admin', False)

        # Check if the current user or an admin is trying to update user information
        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized action.'}, 403

        user_data = api.payload

        # Check if user is trying to modify email or password (not allowed)
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password.'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        updated_user = facade.update_user(user_id, user_data)
        if updated_user:
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        return {'error': 'internal server error'}, 500

    @api.response(200, 'User deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @jwt_required()
    def delete(self, user_id):
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        # Set is_admin default to False if not exists
        is_admin = claims.get('is_admin', False)

        # Check if the current user or an admin is trying to update user information
        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized action.'}, 403

        try:
            facade.delete_user(user_id)
            return {"message": "User deleted successfully"}, 200
        except UserNotFoundError:
            return {"error": "User not found"}, 404


@api.route('/email/<string:email>')
class UserByEmail(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, email):
        """Get user details by email"""
        user = facade.get_user_by_email(email)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200


# @api.route('/protected')
# class ProtectedResource(Resource):
#     @jwt_required()
#     def get(self):
#          """A protected endpoint that requires a valid JWT token"""
#          print("jwt------")
#          print(get_jwt_identity())
#          current_user = get_jwt_identity() # Retrieve the user's identity from the token
#          #if you need to see if the user is an admin or not, you can access additional claims using get_jwt() :
#          # addtional claims = get_jwt()
#          #additional claims["is_admin"] -> True or False
#          return {'message': f'Hello, user {current_user}'}, 200

@api.route('/<user_id>/places')
class UserPlaces(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a list of the users places"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {'places': [
            {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'amenities': [amenity.name for amenity in place.amenities],
                'reviews': [{
                    'text': review.text,
                    'rating': review.rating
                } for review in place.reviews],
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat()
            }
            for place in user.places
        ]}, 200
