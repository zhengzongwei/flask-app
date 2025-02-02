#  Copyright (c)2024. zhengzongwei
#  flask-app-backend is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
#  EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
#  MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.

import datetime

from sqlalchemy import ForeignKey
from app.extensions import db
from app.models.base import BaseModel
from sqlalchemy.orm import relationship


class Book(BaseModel, db.Model):
    __tablename__ = "db_books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="Book ID")
    name = db.Column(db.String(255), nullable=False, comment="Book Name")
    count_page = db.Column(db.String(10), comment="Book Count Page")
    publication_date = db.Column(db.Date)
    isbn = db.Column(db.String(20), unique=True, comment="ISBN")
    version = db.Column(db.String(10), comment="Book Version")
    url = db.Column(db.String(50), comment="Book URL")
    is_deleted = db.Column(db.Boolean, default=False)
    authors = relationship("Author", secondary="book_m2m_author", backref='books', cascade="all, delete")

    # publisher = relationship("Publish", secondary="book_m2m_publish", back_populates='books')


# class Publish(BaseModel, db.Model):
#     """出版社"""
#     __tablename__ = "publisher"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     books = relationship("Book", secondary="book_m2m_publish", back_populates="publisher")


class Author(BaseModel, db.Model):
    __tablename__ = "db_authors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    name = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(11))
    addr = db.Column(db.String(80))
    is_deleted = db.Column(db.Boolean, default=False)
    # books = relationship("Book", secondary="book_m2m_author", back_populates="authors")


class Book_m2m_author(db.Model):
    __tablename__ = "book_m2m_author"
    book_id = db.Column(db.Integer, ForeignKey("db_books.id"), primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey("db_authors.id"), primary_key=True)