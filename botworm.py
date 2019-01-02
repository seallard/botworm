import praw
import re

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

        keywords = ['series','of','the', 'a', 'at', 'to'] # Common lower-case title words.
        word = words_and_punctuation[index-title_index]
        
        # Assume title consists of words before "by" that are uppercase or keywords.
        while word.istitle() and title_index<=limit or word in keywords:
            title = word + " " + title
            title_index += 1
            word = words_and_punctuation[index-title_index] 
        
        if len(title)>1:
            books.append(title + author)
            print(title + author)

    return books

book_list = []

# Iterate over comments and extract titles. 
for submission in subreddit.hot(limit=3):
    for comment in submission.comments:

        if hasattr(comment, "body"):
            books = extract_book(comment.body)
            
            if books != None and books != []:
                book_list.append(books)