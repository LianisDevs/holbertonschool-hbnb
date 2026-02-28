from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

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
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """Register a new place"""
        try:
            place_data = request.get_json()
            
            # Validate required fields
            required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id', 'amenities']
            for field in required_fields:
                if field not in place_data:
                    return {'error': f'Missing required field: {field}'}, 400
            
            # Check if owner exists
            owner = facade.user_repo.get(place_data['owner_id'])
            if not owner:
                return {'error': 'Owner not found'}, 404
            
            # Validate amenities exist
            amenity_objects = []
            for amenity_id in place_data['amenities']:
                amenity = facade.amenity_repo.get(amenity_id)
                if not amenity:
                    return {'error': f'Amenity with id {amenity_id} not found'}, 404
                amenity_objects.append(amenity)
            
            # Create place using facade
            place = facade.create_place(place_data['owner_id'], place_data)
            if not place:
                return {'error': 'Failed to create place'}, 400
            
            # Add amenities to the place
            for amenity in amenity_objects:
                place.add_amenity(amenity)
            
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner,
                'amenities': [amenity.id for amenity in place.amenities],
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat()
            }, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Internal server error'}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.place_repo.get_all()
            places_list = []
            
            for place in places:
                # Get owner details
                owner = facade.user_repo.get(place.owner)
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
                    'created_at': place.created_at.isoformat(),
                    'updated_at': place.updated_at.isoformat()
                }
                places_list.append(place_data)
            
            return places_list, 200
            
        except Exception:
            return {'error': 'Internal server error'}, 500

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.place_repo.get(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Get owner details
            owner = facade.user_repo.get(place.owner)
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
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat()
            }
            
            return place_data, 200
            
        except Exception:
            return {'error': 'Internal server error'}, 500

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            place = facade.place_repo.get(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            update_data = request.get_json()
            
            # Validate owner_id if provided
            if 'owner_id' in update_data:
                owner = facade.user_repo.get(update_data['owner_id'])
                if not owner:
                    return {'error': 'Owner not found'}, 404
            
            # Validate amenities if provided
            if 'amenities' in update_data:
                amenity_objects = []
                for amenity_id in update_data['amenities']:
                    amenity = facade.amenity_repo.get(amenity_id)
                    if not amenity:
                        return {'error': f'Amenity with id {amenity_id} not found'}, 404
                    amenity_objects.append(amenity)
                
                # Update amenities
                place.amenities = amenity_objects
                # Remove amenities from update data as it's handled separately
                del update_data['amenities']
            
            # Update place using facade
            facade.place_repo.update(place_id, update_data)
            
            # Get updated place
            updated_place = facade.place_repo.get(place_id)
            
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner,
                'amenities': [amenity.id for amenity in updated_place.amenities],
                'created_at': updated_place.created_at.isoformat(),
                'updated_at': updated_place.updated_at.isoformat()
            }, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Internal server error'}, 500