from utils.base import engine, Base, session_factory
from sqlalchemy.sql import exists
from models.post import RedditPost
from models.book import Book
from models.comment import Comment


class RecommendationTracker:

    def __init__(self):
        self.session = session_factory()

    def add(self, data):
        self.session.add(data)
        self.session.commit()
        self.session.close()

    def track_post(self, post):
        post = RedditPost(post)
        stmt = exists().where(RedditPost.id==post.id)
        post_exists = self.session.query(stmt).scalar()

        if not post_exists:
            self.add(post)

    def track_comment(self, comment):
        self.session.merge(comment)
        self.session.commit()
        self.session.close()

    def post_exists(self, post_id):
        stmt = exists().where(RedditPost.id==post_id)
        post_exists = self.session.query(stmt).scalar()
        return post_exists

    def number_of_comments_stored(self, post_id):
        return self.session.query(Comment).filter(Comment.post_id == post_id).count()
