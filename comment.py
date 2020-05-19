import re

class Comment:

    def __init__(self, comment):
        self.text = comment.body
        self.author = comment.author
        self.comment_id = comment.id
        self.post_id = comment.submission.id
        self.clean_text = self.__remove_punctuation()
        self.url = self.__create_url()


    def get_mentioned_books(self):
        """ Extract titles from comment. """
        by_indices = self.__find_by_indices()
        books = []
        for index in by_indices:
            book_author = self.__extract_author(index)
            book_title = self.__extract_title(index)

            if len(book_title) > 1 and len(book_author) > 1:
                books.append(book_title + " " + book_author)
        return books


    def __remove_punctuation(self):
        pattern = re.compile(r"[\w']+|[.,!?;]+|\n\n")
        return pattern.findall(self.text)


    def __find_by_indices(self):
        """ Return list of indices at which "by" occurs. """
        by_indices = [i for i, x in enumerate(self.clean_text) if x == "by"]
        return by_indices


    def __extract_author(self, index):
        return " ".join(self.clean_text[index+1:index+3])


    def __extract_title(self, index):
        title = ""
        title_index = 1
        word = self.clean_text[index-title_index]
        limit = len(self.clean_text[:index])

        while title_index <= limit and word.istitle() or self.__is_keyword(word):
            title = word + " " + title
            title_index += 1
            word = self.clean_text[index-title_index]

        return title


    def __is_keyword(self, word):
        keywords = ['of', 'the', 'a', 'at', 'to']
        return word in keywords


    def __create_url(self):
        return f"https://www.reddit.com/comments/{self.post_id}/_/{self.comment_id}/)"