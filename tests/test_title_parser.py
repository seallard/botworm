import pytest
from utils.book_title_parser import BookTitleParser

parser = BookTitleParser()

def test_single():
    text = "Hot Pterodactyl Boyfriend by Alan Cumyn."
    books = parser.extract_titles(text)
    assert books == ["Hot Pterodactyl Boyfriend Alan Cumyn"]

def test_multiple():
    text = "A New Earth by Eckhart Tolle, The Astonishing Power of Emotions by Esther Hicks and The Four Agreements by Don Miguel Ruiz."
    books = parser.extract_titles(text)
    assert books == ["A New Earth Eckhart Tolle", "The Astonishing Power of Emotions Esther Hicks",
                     "The Four Agreements Don Miguel Ruiz"]

def test_sentiment():
    text = "Tales of the Unexpected by Roald Dahl!!! He is such a great author"
    books = parser.extract_titles(text)
    assert books == ["Tales of the Unexpected Roald Dahl"]
