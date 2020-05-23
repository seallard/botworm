import re

class Comment:

    def __init__(self, text, author, comment_id, post_id):
        self.text = text
        self.author = author
        self.comment_id = comment_id
        self.post_id = post_id
        self.url = self.__create_url()

    def __create_url(self):
        return f"https://www.reddit.com/comments/{self.post_id}/_/{self.comment_id}/"
