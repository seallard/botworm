import praw
import pickle
from comment import Comment


class Reddit:

    def __init__(self, user_agent, subreddit):
        self.client = praw.Reddit(user_agent)
        self.subreddit = self.client.subreddit(subreddit)
        self.post_ids = self.__get_commented_posts()

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
                comments.append(Comment(comment))
        return comments


    def post_comments(self, post, comments):
        post_id = post.id
        for comment in comments:
            post = post.reply(comment)
        self.__update_commented_posts(post_id)


    def __get_commented_posts(self):
        try:
            with open ('post_ids', 'rb') as f:
                post_ids = pickle.load(f)
                return post_ids
        except:
            return []


    def __update_commented_posts(self, post_id):
            post_ids.append(post_id)
            with open('post_ids', 'wb') as f:
                pickle.dump(post_ids, f)


    def __worth_checking(self, post):
        return post.id not in self.post_ids and post.num_comments > self.comment_threshold


    def create_table(self, recommendations):

        comments = []
        table = ""
        message = "Hi, I'm a bot! Here are some of the books mentioned in this thread on Goodreads:\n\n"
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