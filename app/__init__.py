from flask import Flask, request

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
from app import views
