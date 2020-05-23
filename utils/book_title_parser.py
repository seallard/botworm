import re

class BookTitleParser:

    def __init__(self):
        self.__clean_text = ""

    def extract_titles(self, text):
        """ Extract titles from text. """
        self.__clean_text = self.__remove_punctuation(text)
        by_indices = self.__find_by_indices()
        books = []
        for index in by_indices:
            book_author = self.__get_author(index)
            book_title = self.__get_title(index)

            if len(book_title) > 1 and len(book_author) > 1:
                books.append(book_title + book_author)
        return books

    def __remove_punctuation(self, text):
        pattern = re.compile(r"[\w']+|[.,!?;]+|\n\n")
        return pattern.findall(text)

    def __find_by_indices(self):
        """ Return list of indices at which "by" occurs. """
        by_indices = [i for i, x in enumerate(self.__clean_text) if x == "by"]
        return by_indices

    def __get_author(self, index):
        author = ""

        if self.__valid_index(index+1):
            first_name = self.__clean_text[index+1]

            if first_name.istitle():
                author += first_name

        if self.__valid_index(index+2):
            last_name = self.__clean_text[index+2]

            if last_name.istitle():
                author += " " + last_name
        return author

    def __valid_index(self, index):
        return index < len(self.__clean_text)

    def __get_title(self, index):
        title = ""
        title_index = 1
        word = self.__clean_text[index-title_index]
        limit = len(self.__clean_text[:index])

        while title_index <= limit and word.istitle() or self.__is_keyword(word):
            title = word + " " + title
            title_index += 1
            word = self.__clean_text[index-title_index]

        return title

    def __is_keyword(self, word):
        keywords = ['of', 'the', 'a', 'at', 'to']
        return word in keywords