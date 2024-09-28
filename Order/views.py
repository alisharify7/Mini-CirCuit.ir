from flask import request, redirect, flash, url_for

from . import order
from . import model as OrderModel

from Web.Apps.OrderPCB.form import OrderICForm
from Core.utils import make_file_name_secure

from Auth.Access import login_required


@order.route("/pcb/", methods=["POST"])
@login_required
def register_pcb_order_post():
    """ register a pcb order for user """
    form = OrderICForm()
    # there is no need captcha for order,
    if not form.validate():
        flash("برخی موارد به درستی وارد نشده است", "danger")
        return redirect(url_for(""))

    user = request.user_object

