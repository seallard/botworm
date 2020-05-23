from utils.reddit import Reddit
from utils.goodreads import Goodreads
from utils.book_title_parser import BookTitleParser
from models.recommendation import Recommendation


def main():
    reddit = Reddit("bot1", "suggestmeabook")
    goodreads = Goodreads()
    title_parser = BookTitleParser()


    for post in reddit.get_posts():

        recommendations = []

        for comment in reddit.get_comments(post):
            mentioned_books = title_parser.extract_titles(comment.text)

            for title in mentioned_books:
                print(title)
                book = goodreads.get_book(title)

                if book != None:
                    recommendations.append(Recommendation(book, comment))

        recommendations.sort(key=lambda x: x.book.rating, reverse=True)
        tables = reddit.create_table(recommendations)
        reddit.post_comments(post, tables)


if __name__ == "__main__":
    main()
