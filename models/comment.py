from sqlalchemy import Table, Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from utils.base import Base
from models.association_tables import comments_books_association


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(String, primary_key=True)
    date = Column(Date)
    post_id = Column(String, ForeignKey('posts.id'))
    by_bot = Column(Boolean)

    books = relationship("Book", secondary=comments_books_association, back_populates="comments")

    def __init__(self, text, author, id, post_id, date, by_bot=False):
        self.text = text
        self.author = author
        self.id = id
        self.post_id = post_id
        self.url = self.__create_url()
        self.date = date
        self.by_bot = by_bot

    def __create_url(self):
        return f"https://www.reddit.com/comments/{self.post_id}/_/{self.id}/"
