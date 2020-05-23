import pytest
from objects.comment import Comment

@pytest.fixture
def single_title_comment():
    text = "Hot Pterodactyl Boyfriend by Alan Cumyn."
    return Comment(text, "redditor", 1, 1)

@pytest.fixture
def multiple_title_comment():
    text = "A New Earth by Eckhart Tolle, The Astonishing Power of Emotions by Esther Hicks and The Four Agreements by Don Miguel Ruiz."
    return Comment(text, "redditor", 1, 1)

@pytest.fixture
def sentiment_comment():
    text = "Tales of the Unexpected by Roald Dahl!!! He is such a great author"
    return Comment(text, "redditor", 1, 1)


def test_basic(single_title_comment):
    books = single_title_comment.get_mentioned_books()
    assert books == ["Hot Pterodactyl Boyfriend Alan Cumyn"]

def test_multiple(multiple_title_comment):
    books = multiple_title_comment.get_mentioned_books()
    assert books == ["A New Earth Eckhart Tolle", "The Astonishing Power of Emotions Esther Hicks",
                    "The Four Agreements Don Miguel Ruiz"]

def test_complex(sentiment_comment):
    books = sentiment_comment.get_mentioned_books()
    assert books == ["Tales of the Unexpected Roald Dahl"]
