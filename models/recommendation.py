
class Recommendation:

    def __init__(self, book, comment):
        self.book = book
        self.comment = comment

    def to_string(self):
        title = self.book.title
        book_url = self.book.url
        author = self.book.author
        reads = str(self.book.count)
        rating = str(self.book.rating)
        redditor = self.comment.author
        comment_url = self.comment.url

        return f"[{title}]({book_url}) | {author} | {reads} | {rating} | [{redditor}]({comment_url})\n"
