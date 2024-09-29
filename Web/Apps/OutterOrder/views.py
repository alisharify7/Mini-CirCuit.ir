from flask import render_template, request, flash, current_app

from . import blp
from .form import RegisterOrderAboardForm

from Auth.Access import login_required
from Core.utils import make_file_name_secure


@blp.route("/", methods=["GET"])
def index_get():
    """return blp register order page"""
    form = RegisterOrderAboardForm()
    return render_template("OutterOrder/order-aboard.html", form=form)


@blp.route("/", methods=["POST"])
@login_required
def index_post():
    """register new order for aboard buying"""
    form = RegisterOrderAboardForm()
    if not form.validate():
        return render_template("OutterOrder/order-aboard.html", form=form)

    if not current_app.extensions["captcha2"].is_verify():
        form.Description.errors.append("کپچا به درستی وارد نشده است")
        flash("کپچا به درستی وارد نشده است", "danger")
        return render_template("OutterOrder/order-aboard.html", form=form)

    order_type = OrderTypes.get_order(type="buy-aboard")
    order = Order()

    if file := request.files.get(form.File.name):
        file_name = make_file_name_secure(file.filename)
    if file:
        order.set_files(file_name)
