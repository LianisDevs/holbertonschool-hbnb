from flask_restx import Namespace, Resource, fields
from werkzeug.wrappers import response
from app.services import facade
from app.utils.errors.place_errors import PlaceNotFoundError
from app.utils.errors.review_errors import ReviewAlreadyExistsError, ReviewInvalidDataError, ReviewNotFoundError
from app.utils.errors.user_errors import UserNotFoundError

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})
@api.route('/setup_mock')
class Mock(Resource):
    def get(self):
        user = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "johnsmith@gmail.com"
        }
        user = facade.create_user(user)

        place = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user.id
        }

        place = facade.create_place(user.id, place)
        return {
            "user_id": user.id,
            "place_id": place.id
        }, 200


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload

        try:
            new_review = facade.create_review(review_data["user_id"], review_data["place_id"], review_data)
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
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        try:
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {"error": "Invalid input data", "message": str(e)}, 400
        except TypeError as e:
            return {"error": "Invalid input data", "message": str(e)}, 400
        except ReviewNotFoundError:
            return {"error": "Review not found"}, 404
        except ReviewInvalidDataError:
            return {"error": "Invalid input data", "message": str(e)}, 400


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ReviewNotFoundError:
            return {"error": "Review not found"}, 404
