import praw
import pickle
from models.comment import Comment


class Reddit:

    def __init__(self, user_agent, subreddit):
        self.client = praw.Reddit(user_agent)
        self.subreddit = self.client.subreddit(subreddit)

        self.time_filter = "week"
        self.post_limit = 50
        self.comment_threshold = 50
        self.char_limit = 9800

    def get_posts(self):
        posts = []
        for post in self.subreddit.top(time_filter=self.time_filter, limit=self.post_limit):
            if self.__worth_checking(post):
                posts.append(post)
        return posts

    def get_comments(self, post):
        comments = []
        for comment in post.comments.list():

            if hasattr(comment, "body"):

                text = comment.body
                author = comment.author
                comment_id = comment.id
                post_id = comment.submission.id
                date = comment.created_utc

                comment = Comment(text, author, comment_id, post_id, date)
                comments.append(comment)
        return comments

    def post_comments(self, post, comments):
        for comment in comments:
            post = post.reply(comment)

    def __worth_checking(self, post):
        return post.num_comments > self.comment_threshold

    def create_table(self, recommendations):

        comments = []
        table = ""
        message = "Here are some of the books mentioned in this thread on Goodreads:\n\n"
        table_header = "Title | Author | Reads | Rating | Comment\n :--|:--|:--|:--|:--\n"

        table += message + table_header

        for recommendation in recommendations:

            if len(table) > self.char_limit:
                comments.append(table)
                table = ""
                table += table_header

            table += recommendation.to_string()

        comments.append(table)
        return comments
