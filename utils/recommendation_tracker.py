from utils.base import engine, Base, session_factory
from sqlalchemy.sql import exists
from models.post import RedditPost
from models.book import Book
from models.comment import Comment
import json

class RecommendationTracker:

    def __init__(self):
        self.session = session_factory()
        self.__read_config()

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

    def __post_exists(self, post_id):
        stmt = exists().where(RedditPost.id==post_id)
        post_exists = self.session.query(stmt).scalar()
        return post_exists

    def comment_exists(self, comment_id):
        stmt = exists().where(Comment.id==comment_id)
        comment_exists = self.session.query(stmt).scalar()
        return comment_exists

    def number_of_comments_stored(self, post_id):
        return self.session.query(Comment).filter(Comment.post_id == post_id).count()

    def most_recent_comment_by_bot(self, post_id):
        return self.session.query(Comment).\
                    filter(Comment.post_id == post_id).\
                    filter(Comment.by_bot == True).\
                    order_by(Comment.date.desc()).first()

    def bot_has_commented(self, post_id):
        if self.most_recent_comment_by_bot(post_id):
            return True
        return False

    def filter_posts(self, posts):
        filtered_posts = []
        for post in posts:
            if self.__post_should_be_checked(post):
                filtered_posts.append(post)
        return filtered_posts

    def filter_comments(self, comments):
        post_id = comments[0].post_id

        # If no table has been posted, all comments are to be checked.
        if not self.most_recent_comment_by_bot(post_id):
            return comments

        filtered_comments = []
        for comment in comments:
            if self.__comment_should_be_checked(comment):
                filtered_comments.append(comment)
        return filtered_comments

    def __post_should_be_checked(self, post):
        if not self.__post_exists(post.id):
            return True

        old = self.number_of_comments_stored(post.id)
        new = post.num_comments

        return new/old >= self.new_comments_ratio

    def __comment_should_be_checked(self, comment):
        return not self.comment_exists(comment.id)

    def __read_config(self):
        with open('configs/config.json') as config_file:
                config = json.load(config_file)
                self.new_comments_ratio = config["new_comments_ratio"]
