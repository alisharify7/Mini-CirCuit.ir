from flask import Blueprint

blp = Blueprint(
    'orderPCB',
    __name__,
    template_folder="templates/order_pcb"
)

from . import views
