from part3.app.models.review import Review
from part3.app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
