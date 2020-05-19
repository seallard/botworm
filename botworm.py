from reddit import Reddit
from goodreads import Goodreads


if __name__ == "__main__":

    reddit = Reddit("bot1", "suggestmeabook")
    goodreads = Goodreads()


    for post in reddit.get_posts():
        for comment in reddit.get_comments(post):

            titles = comment.get_mentioned_books()

            for query in titles:
                book = goodreads.get_book(query)