from flask import Blueprint

blog = Blueprint(
    "blog",
    __name__,
    template_folder="templates/blog",
)

from . import views
from . import model


from .api import bp

blog.register_blueprint(bp, url_prefix="/api/")
