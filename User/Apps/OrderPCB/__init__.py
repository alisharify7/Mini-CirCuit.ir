from flask import Blueprint

OrderIC = Blueprint(
    'orderPCB',
    __name__,
    template_folder="templates",
    static_folder="static"
)

from . import views
