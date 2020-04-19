FROM python:3
WORKDIR /app
COPY . .
RUN pip install praw
CMD [ "python", "./botworm.py" ]