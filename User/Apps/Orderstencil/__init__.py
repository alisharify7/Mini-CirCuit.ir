from flask import Blueprint

OrderStencil = Blueprint(
    "orderstencil",
    __name__,
    template_folder="templates",
    static_folder="static",
)

from . import views
