import praw
import requests
import xml.etree.ElementTree as ET
from operator import itemgetter
import pickle
import goodreads_config
import schedule
import re

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("suggestmeabook")


def clean_comment(comment):
    """
    Remove punctuation and newline chars.
    """

    pattern = re.compile(r"[\w']+|[.,!?;]+|\n\n")
    return pattern.findall(comment)


def find_by_indices(clean_comment):
    """
    Return list of indices at which "by" occurs.
    """

    by_indices = [i for i, x in enumerate(clean_comment) if x == "by"]
    return by_indices


def is_keyword(word):
    """
    Check if the word is a common lowercase word in a title.
    """

    keywords = ['of', 'the', 'a', 'at', 'to']
    return word in keywords


def extract_author(comment, by_index):
    """
    Return author from comment given index of "by".
    It is assumed that the author consists of the two preceeding words.
    """

    return " ".join(comment[by_index+1:by_index+3])


def extract_title(comment, by_index):

    title = ""
    title_index = 1
    word = comment[by_index-title_index]
    limit = len(comment[:by_index])

    while title_index <= limit and word.istitle() or is_keyword(word):
        title = word + " " + title
        title_index += 1
        word = comment[by_index-title_index]

    return title


def extract_books(comment):
    """
    Return list of tuples of the format (title, author) of all books
    found in the comment.
    """

    comment = clean_comment(comment)
    by_indices = find_by_indices(comment)

    # No titles of expected format found.
    if len(by_indices) == 0:
        return None

    books = []

    for index in by_indices:
        author = extract_author(comment, index)
        title = extract_title(comment, index)

        if len(title) > 1 and len(author) > 1:
            books.append((title, author))

    return books


def fetch_goodreads(mentioned_books, users, comment_ids, post_id):
    """
    Find titles on goodreads, return all matches sorted by number of reads.
    """

    base_url = "https://www.goodreads.com/search/index.xml?key=" + goodreads_config.api_key + "&q="

    goodreads_matches = []
    rating_limit = 2.0
    reads_limit = 50
    titles = []

    for i, books in enumerate(mentioned_books):

        user = users[i]
        comment_id = comment_ids[i]

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

                    gr_title = child.find('best_book').findtext('title').split("(")[0].split(":")[0].split(",")[0]
                    author = child.find('best_book').find('author').findtext('name')
                    book_id = child.find('best_book').findtext('id')

                    link = "https://www.goodreads.com/book/show" + book_id
                    comment = "[{}](https://www.reddit.com/comments/{}/_/{}/)".format(user, post_id, comment_id)

            if match:
                data = (gr_title, author, max_reads, rating, link, comment)

                if gr_title not in titles and float(rating) > rating_limit and max_reads > reads_limit:
                    goodreads_matches.append(data)
                    titles.append(gr_title)

    sorted_books = sorted(goodreads_matches, key=itemgetter(3), reverse=True)
    return sorted_books


def create_comments(sorted_books):
    """
    Creates comments (max 10000 chars) of titles in markdown format.
    """

    comments = []
    comment = ""
    message = "Hi, I'm a bot! Here are some of the books mentioned in this thread on Goodreads:\n\n"
    table_header = "Title | Author | Reads | Rating | Comment\n :--|:--|:--|:--|:--\n"

    comment += message + table_header

    for book in sorted_books:

        if len(comment) > 9750: # 10 000 char/comment limit.
            comments.append(comment)
            comment = ""
            comment += table_header

        title, author, reads, rating, link, redditor = book
        row = ("[{}]({}) | {} | {} | {} | {}\n").format(title, link, author, str(reads), rating, redditor)

        comment += row

    comments.append(comment)
    return comments


def main():

    try:
        with open ('post_ids', 'rb') as f:
            post_ids = pickle.load(f)

    except:
        post_ids = []

    time_limit = "week"
    post_limit = 50

    for submission in subreddit.top(time_filter=time_limit, limit=post_limit):

        post_id = submission.id
        mentioned_books = []
        users = []
        comment_ids = []


        if post_id not in post_ids and submission.num_comments > 100 and not submission.archived:

            for comment in submission.comments.list():

                if hasattr(comment, "body"):
                    books = extract_books(comment.body)

                    if books != [] and books != None:
                        mentioned_books.append(books)
                        users.append(comment.author)
                        comment_ids.append(comment.id)
        print(mentioned_books)

        if mentioned_books not in [None, []] and len(mentioned_books) > 10:
            sorted_books = fetch_goodreads(mentioned_books, users, comment_ids, post_id)
            comments = create_comments(sorted_books)

            for comment in comments:
                submission = submission.reply(comment)

            post_ids.append(post_id)
            #with open('post_ids', 'wb') as f:
            #   pickle.dump(post_ids, f)

if __name__ == "__main__":
    main()