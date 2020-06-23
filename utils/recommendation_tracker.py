from utils.base import engine, Base, session_factory
from sqlalchemy.sql import exists
from models.post import RedditPost
from models.book import Book
from models.comment import Comment


class RecommendationTracker:

    def __init__(self):
        self.session = session_factory()

    def add(self, data):
        try:
            self.session.add(data)
            self.session.commit()
            self.session.close()
        except:
            pass

    def track_post(self, post):
        post = RedditPost(post)
        stmt = exists().where(RedditPost.id==post.id)
        post_exists = self.session.query(stmt).scalar()

        if not post_exists:
            self.add(post)

    def track_comment(self, comment):
        stmt = exists().where(Comment.id==comment.id)
        comment_exists = self.session.query(stmt).scalar()

        if not comment_exists:
            self.add(comment)

    def track_book(self, book):
        stmt = exists().where(Book.id==book.id)
        book_exists = self.session.query(stmt).scalar()

        if not book_exists:
            self.add(book)

    def date_of_most_recent_stored_comment(self, post_id):
        pass

    def number_of_comments_stored(self, post_id):
        pass
