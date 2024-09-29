from flask import Blueprint

stencil = Blueprint(
    "stencil",
    __name__,
    template_folder="templates/admin-sub-users",
)

from . import views
