
class Book():

    def __init__(self, title, author, rating, count, goodreads_id):
        self.title = title
        self.author = author
        self.rating = rating
        self.count = count
        self.id = goodreads_id
        self.url = self.__create_url()


    def __create_url(self):
        return "https://www.goodreads.com/book/show/" + str(self.id)