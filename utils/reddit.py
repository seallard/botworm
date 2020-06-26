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

        bot_comment = self.get_bot_comment(post)
        if bot_comment:
            filter_date = datetime.utcfromtimestamp(bot_comment.created_utc)
        else:
            filter_date = datetime(1989, 11, 9)

        comments = []
        for comment in post.comments.list():

            if hasattr(comment, "body"):
                text = comment.body
                author = comment.author
                comment_id = comment.id
                post_id = comment.submission.id
                date = datetime.utcfromtimestamp(comment.created_utc)

                if date > filter_date:
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

    def edit_table(self):
        pass

    def get_bot_comment(self, post):
        for comment in post.comments:
            if not comment.author:
                continue
            if comment.author.name == self.username:
                return comment

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