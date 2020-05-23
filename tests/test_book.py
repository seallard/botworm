import pytest
import requests
from models.book import Book

@pytest.fixture
def example_book():
    title = "The DevOps Handbook: How to Create World-Class Agility, Reliability, and Security in Technology Organizations"
    author = "Kim Gene"
    rating = 4.35
    count = 2713
    gr_id = 26083308
    return Book(title, author, rating, count, gr_id)


def test_title_formatting(example_book):
    assert example_book.title == "The DevOps Handbook"


def test_url_validity(example_book):
    response = requests.get(example_book.url)
    assert response.status_code == 200
