from flask import Blueprint

user = Blueprint(
    "user",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="UserPublicStatic",
)

from . import views

# Register sub application
from .Apps.OrderPCB import OrderIC

user.register_blueprint(OrderIC, url_prefix="/order/printed-integrated-circuit/")

from .Apps.Orderstencil import OrderStencil

user.register_blueprint(OrderStencil, url_prefix="/order/stencils/")
