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

    filtered_posts = tracker.filter_posts(reddit.get_posts())

    for post in filtered_posts:

        tracker.track_post(post)
        lister = RecommendationLister()


        filtered_comments = tracker.filter_comments(reddit.get_comments(post))

        for comment in filtered_comments:
            title_strings = title_parser.extract_titles(comment.text)

            for title in title_strings:
                book = goodreads.get_book(title)

                if book:
                    print("Added book: " + book.title)
                    comment.books.append(book)

            tracker.track_comment(comment)

        recommendations = lister.get()

        if recommendations != []:

            if tracker.bot_has_commented(post.id):
                bot_comment = tracker.most_recent_comment_by_bot(post.id)
                rec_index = reddit.edit_table(bot_comment, recommendations)
                remaining_recommendations = recommendations[rec_index:]

                bot_comments = reddit.create_tables(remaining_recommendations)

                praw_bot_comment = reddit.get_comment(bot_comment.id)
                reddit.post_comments(praw_bot_comment, bot_comments)
                [tracker.track_comment(comment) for comment in bot_comments]

            else:
                bot_comments = reddit.create_tables(recommendations)
                reddit.post_comments(post, bot_comments)
                [tracker.track_comment(comment) for comment in bot_comments]


if __name__ == "__main__":
    main()
