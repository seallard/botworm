from typing import NamedTuple

class Book(NamedTuple):
    title: str
    author: str
    average_rating: float
    ratings_count: int
    goodreads_id: int