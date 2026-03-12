import pytest
from app.models.amenity import Amenity
from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository

class TestAmenityFacade:
    facade = HBnBFacade()

    def setup_method(self):
        """Reset amenities before each test"""
        self.facade.amenity_repo = InMemoryRepository()

    def test_create_amenity(self):
        amenity_data = {"name": "Swimming Pool"}
        amenity = self.facade.create_amenity(amenity_data)
        assert isinstance(amenity, Amenity)
        assert amenity.name == "Swimming Pool"

    def test_get_amenity(self):
        amenity_1 = self.facade.create_amenity({"name": "Pool"})
        amenity_2 = self.facade.create_amenity({"name": "Wi-Fi"})
        amenity = self.facade.get_amenity(amenity_1.id)
        assert isinstance(amenity, Amenity)
        assert amenity.name == "Pool"

    def test_get_all_amenities(self):
        self.facade.create_amenity({"name": "Pool"})
        self.facade.create_amenity({"name": "Wi-Fi"})
        self.facade.create_amenity({"name": "Air Conditioning"})
        amenities = self.facade.get_all_amenities()
        assert isinstance(amenities, list)
        assert len(amenities) == 3
        assert any(a.name == "Pool" for a in amenities)

    def test_update_amenity(self):
        amenity = self.facade.create_amenity({"name": "Pool"})
        updated = self.facade.update_amenity(amenity.id, {"name": "Swimming Pool"})
        assert isinstance(updated, Amenity)
        assert updated.name == "Swimming Pool"

    def test_delete_amenity(self):
        amenity = self.facade.create_amenity({"name": "Pool"})
        deleted = self.facade.delete_amenity(amenity.id)
        assert isinstance(deleted, Amenity)
        assert deleted.name == "Pool"
        assert self.facade.get_amenity(amenity.id) is None

    def test_create_amenity_missing_name(self):
        # Should handle missing name gracefully, return None or raise custom error
        amenity = self.facade.create_amenity({})
        assert amenity is None or isinstance(amenity, Amenity) is False

    def test_update_amenity_not_found(self):
        """Updating a non-existent amenity should return None"""
        updated = self.facade.update_amenity("nonexistent-id", {"name": "New Name"})
        assert updated is None

    def test_update_amenity_empty_name(self):
        """Updating an amenity with empty or whitespace-only name should return None"""
        amenity = self.facade.create_amenity({"name": "Pool"})
        updated = self.facade.update_amenity(amenity.id, {"name": ""})
        assert updated is None