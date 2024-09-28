from flask import make_response

from . import bp

from Blog.model import Post
from Core.extensions import db


@bp.route("/latest/posts/", methods=["GET"])
def get_latest_blog_post():
    """this view return latest blog posts in json format
    uses in index slider
    """
    query = db.session.query(Post).order_by(Post.CreatedTime.desc()).limit(10)
    result = db.session.execute(query)
    return [each.to_dict() for each in result], 200



