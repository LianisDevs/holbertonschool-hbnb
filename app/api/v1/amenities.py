from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        
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
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload

        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {'error': 'Amenity not found'}, 404
        
        for key, value in amenity_data.items():
            if hasattr(amenity, key):
                setattr(amenity, key, value)
            else:
                return {'error': f'Invalid input data: {key}'}, 400
        
        return {"id": amenity.id, "name": amenity.name}, 200