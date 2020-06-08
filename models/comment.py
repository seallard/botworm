from sqlalchemy import Table, Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from utils.database import Base
from models.association_tables import comments_books_association


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    books = relationship("Book", secondary=comments_books_association, backpopulates="comments")

    def __init__(self, text, author, id, post_id):
        self.text = text
        self.author = author
        self.id = id
        self.post_id = post_id
        self.url = self.__create_url()

    def __create_url(self):
        return f"https://www.reddit.com/comments/{self.post_id}/_/{self.id}/"
