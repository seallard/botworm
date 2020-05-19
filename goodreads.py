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

        if r.status_code != 200:
            raise Exception(f"GET query failed: {r.status_code}")

        book_dict = self.__extract_best_hit(r.content)
        book = self.__create_book_object(book_dict)
        sleep(1)
        return book


    def __extract_best_hit(self, xml):
        """ The API returns the books by descending popularity. """
        json = self.__get_content(xml)
        hits = self.__extract_books(json)

        if type(hits) == list:
            return hits[0] # Get the most popular book if more than one hit
        return hits


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
