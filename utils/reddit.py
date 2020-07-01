import praw
import json
from datetime import datetime
from models.comment import Comment


class Reddit:

    def __init__(self):
        self.__read_config()

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
                date = datetime.utcfromtimestamp(comment.created_utc)

                comment = Comment(text, author, comment_id, post_id, date)
                comments.append(comment)
        return comments

    def post_comments(self, post, comments):
        for comment in comments:
            post = post.reply(comment)
            comment.id = post.id

    def get_comment(self, comment_id):
        return self.reddit.comment(id=comment_id)

    def __worth_checking(self, post):
        return post.num_comments > self.comment_threshold

    def create_tables(self, recommendations):
        table = ""
        message = "Here are some of the books mentioned in this thread on Goodreads:\n\n"
        table_header = "Title | Author | Reads | Rating | Comment\n :--|:--|:--|:--|:--\n"
        table += message + table_header

        comment_bodies = []

        for recommendation in recommendations:

            if len(table) > self.char_limit:
                comment_bodies.append(table)
                table = ""
                table += table_header

            table += recommendation.to_string()

        comment_bodies.append(table)

        post_id = recommendation.comment.submission.id
        comments = []

        for text in comment_bodies:
                date = datetime.utcnow()
                comment = Comment(text, "", "", post_id , date)
                comment.by_bot = True
                comments.append(comment)
        return comments

    def __read_config(self):
        with open('configs/config.json') as config_file:

            config = json.load(config_file)

            self.reddit = praw.Reddit(client_id=config["client_id"],
                                      client_secret=config["secret"],
                                      user_agent=config["user_agent"],
                                      username=config["username"],
                                      password=config["password"])

            self.subreddit = self.reddit.subreddit(config["subreddit"])
            self.username = config["username"]

            self.time_filter = config["time_filter"]
            self.post_limit = config["post_limit"]
            self.comment_threshold = config["comment_threshold"]
            self.char_limit = config["char_limit"]