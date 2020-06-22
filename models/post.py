from sqlalchemy import Table, Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from utils.base import Base
from datetime import datetime
from .comment import Comment

class RedditPost(Base):
    __tablename__ = 'posts'

    id = Column(String, primary_key=True)
    date = Date()

    comments = relationship("Comment")

    def __init__(self, post):
        self.id = post.id
        self.date = post.created
