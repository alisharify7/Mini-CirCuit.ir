from flask import Blueprint

blp = Blueprint(
    'outer_order',
    __name__,
    template_folder="templates"
)

from . import views
