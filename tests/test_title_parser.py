import pytest
from utils.book_title_parser import BookTitleParser

@pytest.fixture
def parser():
    return BookTitleParser()

@pytest.fixture
def single_title():
    return "Hot Pterodactyl Boyfriend by Alan Cumyn."

@pytest.fixture
def multiple_titles():
    return "A New Earth by Eckhart Tolle, The Astonishing Power of Emotions by Esther Hicks and The Four Agreements by Don Miguel Ruiz."

@pytest.fixture
def sentiment_title():
    return "Tales of the Unexpected by Roald Dahl!!! He is such a great author"


def test_single(single_title, parser):
    books = parser.extract_titles(single_title)
    assert books == ["Hot Pterodactyl Boyfriend Alan Cumyn"]

def test_multiple(multiple_titles, parser):
    books = parser.extract_titles(multiple_titles)
    assert books == ["A New Earth Eckhart Tolle", "The Astonishing Power of Emotions Esther Hicks",
                     "The Four Agreements Don Miguel Ruiz"]

def test_sentiment(sentiment_title, parser):
    books = parser.extract_titles(sentiment_title)
    assert books == ["Tales of the Unexpected Roald Dahl"]
