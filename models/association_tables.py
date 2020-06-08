from sqlalchemy import Table, Column, String, Integer, Date, ForeignKey
from utils.base import Base

comments_books_association = Table('comments_books', Base.metadata,
    Column('comment_id', String, ForeignKey('comments.id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)
