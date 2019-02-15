import praw
import re
import requests
import xml.etree.ElementTree as ET
import goodreads_config
import csv
from operator import itemgetter
import time

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("suggestmeabook")


def extract_book(comment):
    """
    Returns a list of all titles mentioned in a comment.
    """

    pattern = re.compile(r"[\w']+|[.,!?;]+|\n\n")
    words_and_punctuation = pattern.findall(comment)
    by_indices = [i for i, x in enumerate(words_and_punctuation) if x == "by"]

    if len(by_indices) == 0:
        return None

    books = []

    for index in by_indices:
        author = " ".join(words_and_punctuation[index+1:index+3])

        title = ""
        title_index = 1
        limit = len(words_and_punctuation[:index])

        # Common lower-case title words.
        keywords = ['series', 'of', 'the', 'a', 'at', 'to']
        word = words_and_punctuation[index-title_index]

        # Assume title consists of uppercase/keywords before "by".
        while title_index <= limit and word.istitle() or word in keywords:
            title = word + " " + title
            title_index += 1
            word = words_and_punctuation[index-title_index]

        if len(title) > 1 and len(author) > 1:
            books.append((title, author))

    return books


books_list = []
post_titles = []

print("All search results will be saved to a csv file in this directory.")
rating_limit = float(input("Enter rating cutoff [0-5]: "))
time_limit = input(
    "Enter top time filter [hour, day, week, month, year or all]: ")
post_limit = int(input("Enter number of posts to filter: "))

# Iterate over comments and extract titles.
for submission in subreddit.top(time_filter=time_limit, limit=post_limit):
    post_titles.append(submission.title)
    print("Post title: " + " " + submission.title)
    for comment in submission.comments:

        if hasattr(comment, "body"):
            books = extract_book(comment.body)

            if books is not None and books != []:
                books_list.append(books)

base_url = "https://www.goodreads.com/search/index.xml?key=" + \
    goodreads_config.api_key + "&q="
goodreads_matches = []

# Iterate over extracted titles and search goodreads.
for books in books_list:
    for book in books:

        title, author = book
        query = title + author

        response = requests.get(base_url + query)
        root = ET.fromstring(response.content)

        max_count = 0
        match = False

        for child in root.iter('work'):
            count = int(child.findtext('ratings_count'))

            if count >= max_count:
                match = True
                max_count = count
                rating = child.findtext('average_rating')
                year = child.findtext('original_publication_year')
                gr_title = child.find('best_book').findtext('title')
                book_id = child.find('best_book').findtext('id')
                name = child.find('best_book').find('author').findtext('name')
                link = "https://www.goodreads.com/book/show/"+book_id+".a"

        data = (gr_title, name, int(max_count), rating, link)

        if match and data not in goodreads_matches and float(rating) > rating_limit:
            goodreads_matches.append(data)

            print("Search: " + query)
            print("Match: " + gr_title + " by " + name)
            print("Number of reads: " + str(max_count))
            print("--------")

sorted_books = sorted(goodreads_matches, key=itemgetter(2), reverse=True)
file_name = time.strftime("%Y%m%d")
with open(file_name, "w", newline='') as f:

    f.write("Title | Author | Reads | Rating | Link\n")
    f.write(":--|:--|:--|:--|:--\n")

    for book in sorted_books:
        title, author, reads, rating, link = book
        f.write(("{} | {} | {} | {} | [goodreads]({})\n").format(
            title, author, str(reads), rating, link))
