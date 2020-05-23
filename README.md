# botworm
A Reddit bot that compiles lists of book recommendations from r/suggestmeabook, see [u/Guardian_of_Bookworm](https://www.reddit.com/user/Guardian_of_Bookworm).


## Getting started
To run the bot you need to get access to the API of [Goodreads]() and [Reddit](). Update the config-files with your information.  
Since I'm already running the bot, please comment out the last line in botworm.py as to not post any comments.

To build and run the bot:
```bash
docker build -t botworm .
docker run botworm
```
