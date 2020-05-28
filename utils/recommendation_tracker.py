from models.recommendation import Recommendation

class RecommendationTracker:

    def __init__(self):
        self.__recommendations_dict = {}
        self.__recommendations = []

    def add(self, book, comment):
        if book is not None:
            self.__recommendations_dict[book.title] = Recommendation(book, comment)

    def get(self):
        self.__recommendations = list(self.__recommendations_dict.values())
        self.__sort()
        return self.__recommendations

    def __sort(self):
        self.__recommendations.sort(key=lambda x: x.book.rating, reverse=True)
