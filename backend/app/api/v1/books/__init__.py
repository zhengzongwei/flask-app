from flask import Blueprint

books = Blueprint('books', __name__, url_prefix='/books')

from . import views
