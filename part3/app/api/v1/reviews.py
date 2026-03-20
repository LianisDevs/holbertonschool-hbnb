from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from part3.app.services import facade
from part3.app.utils.errors.place_errors import PlaceNotFoundError
from part3.app.utils.errors.review_errors import ReviewAlreadyExistsError, ReviewInvalidDataError, ReviewNotFoundError
from part3.app.utils.errors.user_errors import UserNotFoundError
import os
from part3.app import db

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/setup_mock')
class Mock(Resource):
    def get(self):
        user = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "johnsmithadmin@gmail.com",
            "password": "123",
        }
        user = facade.create_user(user)

        # place = {
        #     "title": "Cozy Apartment",
        #     "description": "A nice place to stay",
        #     "price": 100.0,
        #     "latitude": 37.7749,
        #     "longitude": -122.4194
        # }
        # print("setting up place")
        #
        # place = facade.create_place(user.id, place)
        return {
            "user_id": user.id,
            # "place_id": place.id
        }, 200


@api.route('/restart_db')
class MockRestart(Resource):
    def delete(self):
        from run import get_app
        database_path = '/Users/moyea/holbertonschool-hbnb/instance/development.db'

        if os.path.exists(database_path):
            os.remove(database_path)
            print(f"Database file '{database_path}' deleted successfully.")
        else:
            print(f"Database file '{database_path}' does not exist.")

        with get_app().app_context():
            db.create_all()


@api.route('/elevate_admin')
class MockAdmin(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        facade.update_user(current_user_id, {"is_admin": True})
        access_token = create_access_token(
            identity=str(current_user_id),   # only user ID goes here
            additional_claims={"is_admin": True}  # extra info here
        )

        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Access forbidden - you cannot review your own place or you have already reviewed this place')
    @jwt_required()
    def post(self):
        """Register a new review"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()

        review_data = api.payload

        # Set user_id from JWT token
        review_data['user_id'] = current_user_id

        try:
            # Check if place exists and get place details
            place = facade.get_place(review_data['place_id'])
            if not place:
                return {"error": "Invalid input data", "message": "Place not found"}, 400

            # Check if user is trying to review their own place
            if place.owner_id == current_user_id:
                return {"error": "You cannot review your own place."}, 400

            # Check if user has already reviewed this place
            existing_reviews = facade.get_reviews_by_place(
                review_data['place_id'])
            for review in existing_reviews:
                if review.user_id == current_user_id:
                    return {"error": "You have already reviewed this place."}, 400

            new_review = facade.create_review(
                review_data["user_id"], review_data["place_id"], review_data)
        except UserNotFoundError as e:
            return {"error": "Invalid input data", "message": str(e)}, 400
        except PlaceNotFoundError as e:
            return {"error": "Invalid input data", "message": str(e)}, 400
        except ReviewAlreadyExistsError as e:
            return {"error": "Invalid input data", "message": str(e)}, 400
        except ValueError as e:
            return {"error": "Invalid input data", "message": str(e)}, 400
        except TypeError as e:
            return {"error": "Invalid input data", "message": str(e)}, 400

        data = new_review.to_json()
        return data, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        data = [review.to_json_id_text_rating() for review in reviews]
        return data, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            fetched_review = facade.get_review(review_id)
            json_fetched_review = fetched_review.to_json()
            return json_fetched_review, 200
        except ReviewNotFoundError:
            return {"error": "Review not found"}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()

        # Get permissions from token
        current_user = get_jwt()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)

        try:
            # Get the review and check ownership
            review = facade.get_review(review_id)
            if not is_admin and review.user_id != current_user_id:
                return {"error": "Unauthorized action."}, 403

            review_data = api.payload
            # Set user_id from JWT token to prevent tampering
            review_data['user_id'] = current_user_id

            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {"error": "Invalid input data", "message": str(e)}, 400
        except TypeError as e:
            return {"error": "Invalid input data", "message": str(e)}, 400
        except ReviewNotFoundError:
            return {"error": "Review not found"}, 404
        except ReviewInvalidDataError as e:
            return {"error": "Invalid input data", "message": str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()

        # Get permissions from token
        current_user = get_jwt()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)

        try:
            # Get the review and check ownership or admin status
            review = facade.get_review(review_id)
            if not is_admin and review.user_id != current_user_id:
                return {"error": "Unauthorized action."}, 403

            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ReviewNotFoundError:
            return {"error": "Review not found"}, 404
