import praw
import re

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("suggestmeabook")

def extract_book(comment):
    """
    Extracts all books from comment string.
    """
    
    comment = re.sub(r'[^a-zA-Z\d\s:]', '', comment)
    word_list = comment.split(' ')
    by_indices = [i for i, x in enumerate(word_list) if x == "by"]
    
    # Check if any book is mentioned. 
    if len(by_indices) == 0:
        return None
    
    # Extract each book.
    books = []

    # Extract first book in comment (fix all later).
    for index in [by_indices[0]]:

        # Get the author.
        author = " ".join(word_list[index+1:index+3])

        # Get title. 
        i = 1
        limit = len(word_list[:index])
        
        while word_list[index-i-1].istitle() and i < limit:
            i += 1

        title = " ".join(word_list[index-i:index])
        title = re.sub(r"\n", "", title)
        
        books.append(title + " " + author)

    return books



for submission in subreddit.hot(limit=2):

    for comment in submission.comments:
        book = extract_book(comment.body.rstrip())
        
        if book != None:      
            print(book)
