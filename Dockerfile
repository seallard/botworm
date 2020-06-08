FROM python:3 as prepare
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM prepare as prod
WORKDIR /app
COPY . .
CMD [ "python", "./botworm.py" ]