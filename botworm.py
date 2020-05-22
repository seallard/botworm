from reddit import Reddit
from goodreads import Goodreads
from recommendation import Recommendation


if __name__ == "__main__":

    reddit = Reddit("bot1", "suggestmeabook")
    goodreads = Goodreads()


    for post in reddit.get_posts():

        recommendations = []

        for comment in reddit.get_comments(post):
            mentioned_books = comment.get_mentioned_books()

            for title in mentioned_books:
                book = goodreads.get_book(title)

                if book != None:
                    recommendations.append(Recommendation(book, comment))

        tables = reddit.create_table(recommendations)
        reddit.post_comments(post, tables)