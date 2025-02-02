#  Copyright (c)2024. zhengzongwei
#  flask-app-backend is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
#  EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
#  MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.

from flask import Blueprint, request

from app.dao.authors import AuthorDao
from app.models.book import Author
from app.schemas.books import AuthorSchema
from app.api.api import success_response, error_response

from app.common.utils.logs import Logger

from app.dao.books import BookDao
from app.exceptions import exceptions
from . import authors_bp as bp

logger = Logger('authors')


# @bp.errorhandler(exceptions.DBException)
# def invalid_api_usage(e):
#     if isinstance(e, HTTPException):
#
#     return error_response(e.message, e.http_code)

@bp.route('/')
@bp.route('/<id>', methods=['GET'])
def authors(id=None):
    if id:
        try:
            book = AuthorDao.get_author_by_id(id)
        except Exception as e:
            return error_response(e.message, e.http_status)
        return AuthorSchema().dump(book)
    else:
        offset = request.args.get('offset', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)
        data = AuthorDao().list_author(offset, limit)
        authors_data = AuthorSchema(many=True).dump(data)
        return success_response(data=authors_data)


@bp.route('/', methods=['POST'])
def create_author():
    data = request.json
    authors_data = data.get("authors", None)
    create_many = False
    if isinstance(authors_data, list):
        create_many = True
    _authors = AuthorSchema().load(authors_data, many=create_many)
    try:
        AuthorDao().create_author(_authors)
    except Exception as e:
        return error_response(e.message, e.http_code)
    return success_response('Author created', 201)


@bp.route('/', methods=['DELETE'])
def delete_author():
    try:
        AuthorDao().delete_author(request.json.get('authors_id', []))
    except Exception as e:
        return error_response(e.message, e.http_code)
    return success_response('Author deleted', 204)


@bp.route('/<int:id>', methods=['PUT'])
def edit_author(id=None):
    author = AuthorSchema(load_instance=False).load(request.get_json(), partial=True, )
    try:
        AuthorDao().edit_author(id, author)
    except Exception as e:
        return error_response(e.message, e.http_code)
    return success_response('Author edited', 204)
