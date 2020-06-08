from utils.base import Base, session_factory
from models.book import Book


class RecommendationTracker:

    def update(self, data):
        session = session_factory()
        session.add(data)
        session.commit()
        session.close()
