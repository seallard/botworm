import requests
from time import sleep
import xmltodict
from json import loads, dumps
import goodreads_config
from book import Book


class Goodreads:

    def __init__(self):
        self.token = goodreads_config.api_key
        self.base = "https://www.goodreads.com"


    def get_book(self, query):
        """ Query the search endpoint of the Goodreads API. """
        search_url = self.base + "/search/index.xml?key=" + self.token + "&q=" + query
        r = requests.get(search_url)
        sleep(1)

        if r.status_code != 200:
            raise Exception(f"GET query failed: {r.status_code}")

        json = self.__get_content(r.content)
        best_hit = self.__get_best_hit(json)

        if best_hit == None:
            print(f"No hit for query: {query}")
            return None

        book = self.__create_book_object(best_hit)
        return book


    def __get_best_hit(self, json):
        number_of_hits = self.__number_of_hits(json)

        if number_of_hits == 0 or number_of_hits == None:
            return None

        if number_of_hits == 1:
            book_dict = self.__extract_books(json)

        if number_of_hits > 1:
            book_dict = self.__extract_books(json)[0]

        return book_dict


    def __number_of_hits(self, json):
        return int(json["GoodreadsResponse"]["search"]["total-results"])


    def __get_content(self, xml):
        """ Convert from xml to json. """
        data = xmltodict.parse(xml)
        json = loads(dumps(data))
        return json


    def __extract_books(self, json):
        """ Extract the list of books from the json response. """
        return json['GoodreadsResponse']['search']['results']['work']


    def __create_book_object(self, book_dict):
        """ Create a book object from the dictionary. """
        title = book_dict["best_book"]["title"]
        author = book_dict["best_book"]["author"]["name"]
        rating = float(book_dict["average_rating"])
        count = int(book_dict["ratings_count"]["#text"])
        goodreads_id = int(book_dict["best_book"]["id"]["#text"])
        return Book(title, author, rating, count, goodreads_id)
