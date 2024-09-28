from flask import render_template, abort, request

from Core.extensions import db
from Admin.utils import get_admin
from Admin.model import Admin

from . import blog
from .model import Post


@blog.route("/", methods=["GET"])
def index_get():
    """ blog main index return all post in  pagination mode
     and order by creation date """
    page = request.args.get(key="page", default=1, type=int)
    query = db.select(Post).order_by(Post.CreatedTime.desc())

    query_result = db.paginate(select=query, per_page=16, page=page, error_out=True)

    ctx = {
        "posts": query_result,
        "current_page": page
    }
    return render_template("blog-list.html", ctx=ctx)


@blog.route("/author/<string:username>/", methods=["GET"])
def author_index_get(username: str) -> str:
    """ author's special page for posts """
    query = db.session.query(Admin).filter_by(Username=username)

    author = db.session.execute(query).scalar_one_or_none()
    if not author:
        abort(404)

    page = request.args.get(key="page", default=1, type=int)

    query = db.session.query(Post).filter_by(AuthorID=author.id).order_by(Post.CreatedTime.desc())
    query_result = db.paginate(select=query, per_page=16, page=page, error_out=True)

    ctx = {
        "author": author,
        "posts": query_result,
        "current_page": page
    }
    return render_template("author-post-list.html", ctx=ctx)


@blog.route("/s/<string:slug>/", methods=["GET"])
def show_post_by_slug_get(slug):
    """ Showing posts base on slug in url """
    query = db.session.query(Post).filter_by(Slug=slug)
    query_result = db.session.execute(query).scalars()
    query_result = db.session.execute(query).sca

    if not query_result:  # TODO: replace it with a custom template like blog post is not found, see similars
        abort(404)

    ctx = {
        "post": query_result,
        "author": get_admin(query_result.AuthorID)
    }

    return render_template("blog-details.html", ctx=ctx)


@blog.route("/<string:title>/", methods=["GET"])
def show_post_by_title_get(title):
    """ Showing posts base on title in url """
    title = title.replace("-", " ")
    query = db.session.query(Post).filter_by(Title=title)
    query_result = db.session.execute(query).scalar_one_or_none()

    if not query_result:  # TODO: replace it with a custom template like blog post is not found, see similars
        abort(404)

    ctx = {
        "post": query_result,
        "author": get_admin(query_result.AuthorID)

    }
    return render_template("blog-details.html", ctx=ctx)
