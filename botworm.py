from utils.reddit import Reddit
from utils.goodreads import Goodreads
from utils.book_title_parser import BookTitleParser
from utils.recommendation_lister import RecommendationLister
from utils.database import Database


def main():

    reddit = Reddit("bot1", "suggestmeabook")
    goodreads = Goodreads()
    title_parser = BookTitleParser()
    database = Database()

    for post in reddit.get_posts():
        lister = RecommendationLister()

        for comment in reddit.get_comments(post):
            mentioned_books = title_parser.extract_titles(comment.text)

            for title in mentioned_books:
                print(title)
                book = goodreads.get_book(title)
                lister.add(book, comment)
                database.test()

        recommendations = lister.get()
        tables = reddit.create_table(recommendations)
        reddit.post_comments(post, tables)


if __name__ == "__main__":
    main()
