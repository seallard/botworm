import requests
from time import sleep
import xmltodict
from json import loads, dumps, load
from models.book import Book



class Goodreads:

    def __init__(self):
        self.__read_config()

    def get_book(self, query):
        """ Query the search endpoint of the Goodreads API. """
        search_url = "https://www.goodreads.com/search/index.xml?key=" + self.token + "&q=" + query
        r = requests.get(search_url)
        sleep(1)

        if r.status_code != 200:
            raise Exception(f"GET query failed: {r.status_code}")

        json = self.__get_content(r.content)
        best_hit = self.__get_best_hit(json)

        if best_hit is None:
            print(f"No hit for query: {query}")
            return None

        book = self.__create_book_object(best_hit)
        return book

    def __get_best_hit(self, json):
        """ Extract the most popular hit. """
        number_of_hits = self.__number_of_hits(json)

        if number_of_hits == 0:
            return None

        books = self.__extract_books(json)
        best_hit = books[0]

        for book in books:
            if int(book["ratings_count"]["#text"]) > int(best_hit["ratings_count"]["#text"]):
                best_hit = book

        if self.__valid(best_hit):
            return best_hit

    def __number_of_hits(self, json):
        return int(json["GoodreadsResponse"]["search"]["total-results"])

    def __valid(self, book_dict):
        count = int(book_dict["ratings_count"]["#text"])
        return count > self.reads_threshold

    def __get_content(self, xml):
        """ Convert from xml to json. """
        data = xmltodict.parse(xml)
        json = loads(dumps(data))
        return json

    def __extract_books(self, json):
        """ Extract the list of books from the json response. """
        books = json['GoodreadsResponse']['search']['results']['work']
        if not type(books) is list:
            books = [books]
        return books

    def __create_book_object(self, book_dict):
        """ Create a book object from the dictionary. """
        title = book_dict["best_book"]["title"]
        author = book_dict["best_book"]["author"]["name"]
        rating = float(book_dict["average_rating"])
        count = int(book_dict["ratings_count"]["#text"])
        goodreads_id = int(book_dict["best_book"]["id"]["#text"])
        return Book(title, author, rating, count, goodreads_id)

    def __read_config(self):
        with open('configs/config.json') as config_file:
            config = load(config_file)
            self.token = config["goodreads_api_key"]
            self.reads_threshold = config["read_threshold"]
