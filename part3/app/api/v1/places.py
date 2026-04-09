from flask import current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from part3.app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
})

place_update_model = api.model('Place', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place'),
})


@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    def post(self):
        try:
            payload = api.payload or {}
            identity = get_jwt_identity()

            owner_id = identity.get("id") if isinstance(identity, dict) else identity
            if not owner_id:
                return {"error": "Unauthorized"}, 401

            required = ["title", "price", "latitude", "longitude"]
            missing = [k for k in required if payload.get(k) is None]
            if missing:
                return {"error": f"Missing fields: {', '.join(missing)}"}, 400

            payload.setdefault("amenities", [])

            place = facade.create_place(owner_id, payload)

            amenities_data = [
                {"id": amenity.id, "name": amenity.name}
                for amenity in place.amenities
            ]

            place_data = {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": float(place.price),
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner_id,
                "amenities": amenities_data,
                "created_at": place.created_at.isoformat(),
                "updated_at": place.updated_at.isoformat()
            }

            return place_data, 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            current_app.logger.exception("Failed to create place")
            return {"error": "Internal server error"}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            places_list = []

            for place in places:
                # Get owner details
                owner = facade.user_repo.get(place.owner_id)
                owner_data = {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                } if owner else None

                # Get amenities details
                amenities_data = []
                for amenity in place.amenities:
                    amenities_data.append({
                        'id': amenity.id,
                        'name': amenity.name
                    })

                place_data = {
                    'id': place.id,
                    'title': place.title,
                    'description': place.description,
                    'owner': owner_data,
                    'price': float(place.price),
                    'amenities': amenities_data,
                    'reviews': [{
                        'text': review.text,
                        'rating': review.rating
                    } for review in place.reviews],
                    'created_at': place.created_at.isoformat(),
                    'updated_at': place.updated_at.isoformat()
                }
                places_list.append(place_data)

            return places_list, 200

        except Exception as e:
            return {'error': 'Internal server error'}, 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Get owner details
            owner = facade.user_repo.get(place.owner_id)
            owner_data = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            } if owner else None

            # Get amenities details
            amenities_data = []
            for amenity in place.amenities:
                amenities_data.append({
                    'id': amenity.id,
                    'name': amenity.name
                })

            place_data = {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': owner_data,
                'amenities': amenities_data,
                'reviews': [{
                    'text': review.text,
                    'rating': review.rating
                } for review in place.reviews],
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat()
            }

            return place_data, 200

        except Exception:
            return {'error': 'Internal server error'}, 500

    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        # Get current user from JWT token
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # Check if the current user is the owner of the place or and admin
            if not is_admin and place.owner_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            update_data = api.payload

            # Update place using facade
            facade.update_place(place_id, update_data)

            # Get updated place
            updated_place = facade.get_place(place_id)

            amenities_data = []
            for amenity in updated_place.amenities:
                amenities_data.append({'id': amenity.id, 'name': amenity.name})

            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner_id,
                'amenities': amenities_data,
                'created_at': updated_place.created_at.isoformat(),
                'updated_at': updated_place.updated_at.isoformat()
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Internal server error'}, 500

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Failed to delete place')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        # Get identity
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        try:
            # 2. Check if place exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            # 3. Check permissions: Admin OR Owner
            if not is_admin and place.owner_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            # 4. Execute deletion using your facade method
            success = facade.delete_place(place_id)

            if success:
                return {'message': 'Place deleted successfully'}, 200
            else:
                return {'error': 'Failed to delete place'}, 400

        except Exception:
            return {'error': 'Internal server error'}, 500


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.place_repo.get(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        data = [review.to_json_id_text_rating() for review in reviews]
        return data, 200
