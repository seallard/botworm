from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship
from utils.base import Base
from models.association_tables import comments_books_association


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    comments = relationship("Comment", secondary=comments_books_association, back_populates="books")

    def __init__(self, title, author, rating, count, goodreads_id):
        self.title = self.__format_title(title)
        self.author = author
        self.rating = rating
        self.count = count
        self.id = goodreads_id
        self.url = self.__create_url()

    def __format_title(self, title):
        """ Remove series name and subtitle. """
        new_title = title.split("(")[0].split(":")[0].split(",")[0].split("by")[0]
        return new_title

    def __create_url(self):
        return "https://www.goodreads.com/book/show/" + str(self.id)
