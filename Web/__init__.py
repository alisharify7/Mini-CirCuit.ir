from flask import Blueprint

web = Blueprint(
    "web",
    __name__,
    static_folder="static/web/",
    template_folder="templates/web/",
    static_url_path="WebPublicStatic",
)

from . import views

from .Apps import OuterOrder

web.register_blueprint(OuterOrder, url_prefix="/buy-from-abroad/")


from .Apps import OrderPCB

web.register_blueprint(OrderPCB, url_prefix="/pcb/")
