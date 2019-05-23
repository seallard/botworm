import praw
import requests
import re
import xml.etree.ElementTree as ET
from operator import itemgetter
import pickle
import goodreads_config


reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("suggestmeabook")


def extract_books(comment):
    """
    Return list of all titles mentioned in a comment.
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


def fetch_goodreads(mentioned_books):
    """
    Find titles on goodreads, return all matches sorted by number of reads.
    """

    print("Collecting Goodreads data...")
    print("Books found in comments: {}".format(sum([len(x) for x in mentioned_books])))

    base_url = "https://www.goodreads.com/search/index.xml?key=" + goodreads_config.api_key + "&q="
    goodreads_matches = []
    rating_limit = 3.0
    reads_limit = 100
    titles = []

    for books in mentioned_books:
        for book in books:

            title, author = book
            query = title + author

            response = requests.get(base_url + query)
            root = ET.fromstring(response.content)

            max_reads = 0
            match = False

            for child in root.iter('work'):
                reads = int(child.findtext('ratings_count'))

                if reads >= max_reads:

                    match = True

                    max_reads = reads
                    rating = child.findtext('average_rating')

                    gr_title = child.find('best_book').findtext(
                        'title').split("(")[0].split(":")[0].split(",")[0]
                    author = child.find('best_book').find(
                        'author').findtext('name')

                    link = "https://www.goodreads.com/book/title?id=" + \
                        gr_title.replace(" ", "%2B")

            if match:
                data = (gr_title, author, int(max_reads), rating, link)

                if gr_title not in titles and float(rating) > rating_limit and max_reads > reads_limit:
                    print(gr_title)

                    goodreads_matches.append(data)
                    titles.append(gr_title)

    sorted_books = sorted(goodreads_matches, key=itemgetter(2), reverse=True)
    print("Books found on goodreads: {}".format(len(sorted_books)))

    return sorted_books


def create_comments(sorted_books):
    """
    Creates comments (max 10000 chars) of titles in markdown format.
    """

    comments = []
    comment = ""
    message = "Some of the books mentioned in this thread on Goodreads:\n\n"
    table_header = "Title | Author | Reads | Rating\n :--|:--|:--|:--|:--\n"

    comment += message + table_header

    for book in sorted_books:

        if len(comment) > 9750:  # 10 000 char/comment limit.
            comments.append(comment)
            comment = ""
            comment += table_header

        title, author, reads, rating, link = book
        row = ("[{}]({}) | {} | {} | {}\n").format(
            title, link, author, str(reads), rating)
        comment += row

    comments.append(comment)

    return comments


def main():

    try:
        with open('post_ids', 'rb') as f:
            post_ids = pickle.load(f)

    except:
        post_ids = []

    time_limit = "month"
    post_limit = 10

    for submission in subreddit.top(time_filter=time_limit, limit=post_limit):

        print(submission.title)

        post_id = submission.id
        mentioned_books = []

        if post_id not in post_ids and submission.num_comments > 95 and not submission.archived:

            post_ids.append(post_id)

            for comment in submission.comments.list():
                if hasattr(comment, "body"):

                    books = extract_books(comment.body)

                    if books != None and books != []:
                        mentioned_books.append(books)

        if mentioned_books not in [None, []]:

            sorted_books = fetch_goodreads(mentioned_books)
            comments = create_comments(sorted_books)

            for comment in comments:
                submission = submission.reply(comment)
                print("Posted comment...")

    with open('post_ids', 'wb') as f:
        pickle.dump(post_ids, f)


main()