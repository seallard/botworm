from utils.reddit import Reddit
from utils.goodreads import Goodreads
from utils.book_title_parser import BookTitleParser
from utils.recommendation_lister import RecommendationLister
from utils.recommendation_tracker import RecommendationTracker


def main():

    reddit = Reddit()
    goodreads = Goodreads()
    title_parser = BookTitleParser()
    tracker = RecommendationTracker()

    for post in reddit.get_posts():

        tracker.track_post(post)
        lister = RecommendationLister()

        for comment in reddit.get_comments(post):
            title_strings = title_parser.extract_titles(comment.text)

            for title in title_strings:
                book = goodreads.get_book(title)

                if book:
                    comment.books.append(book)

            tracker.track_comment(comment)


        recommendations = lister.get()
        bot_comments = reddit.create_tables(recommendations)
        #reddit.post_comments(post, tables)
        [tracker.track_comment(comment) for comment in bot_comments]


if __name__ == "__main__":
    main()
