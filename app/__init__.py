from flask import Flask
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.tweet

app = Flask(__name__)
app.config.from_object('config')

from app import views, models