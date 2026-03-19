from flask_restx import Namespace, Resource, fields
from part3.app.services import facade
from flask_jwt_extended import current_user, get_jwt_identity, jwt_required, get_jwt

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Amenity already exists')
    @api.response(400, 'Missing Required Fields')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new amenity"""

        # Retrieve permissions from the token
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        admin = facade.get_user(current_user_id)

        is_admin = claims.get('is_admin', False)

        # ADMIN CHECK
        if not is_admin:
            return {'error': 'Unauthorized action.'}, 403

        amenity_data = api.payload
        
        name = amenity_data.get("name")
        if not name or not name.strip():
            return {'error': 'missing fields'}, 400

        existing_amenity = None
        for a in facade.get_all_amenities():
            if a.name == amenity_data.get("name"):
                existing_amenity = a
                break

        if existing_amenity:
            return {'error': 'Amenity already exists'}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenity_list = facade.get_all_amenities()
        return [{"id": a.id, "name": a.name} for a in amenity_list], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):

    @api.response(200, 'Amenity retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {'error': 'Amenity not found'}, 404

        return {"id": amenity.id, "name": amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Missing Required Fields')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""

        # Retrieve permissions from the token
        current_user = get_jwt()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)

        # ADMIN CHECK
        if not is_admin:
            return {'error': 'Unauthorized action.'}, 403

        amenity_data = api.payload

        name = amenity_data.get("name")
        if not name or not name.strip():
            return {'error': 'missing fields'}, 400

        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {'error': 'Amenity not found'}, 404
        
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'error': 'Failed to update amenity'}, 400
        return {"id": updated_amenity.id, "name": updated_amenity.name}, 200
