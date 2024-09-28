from flask import render_template, flash

from . import OrderIC

from User.utils import login_required
from Web.Apps.OrderPCB.form import OrderICForm
from Core.extensions import csrf

@OrderIC.route("/", methods=["GET"])
@login_required
def index_get():
    """user menu -> order printed ic page"""
    ctx = {
        "orderICPage": "active"
    }
    form = OrderICForm()
    form.show_file = True
    return render_template("OrderIC/order.html", ctx=ctx, form=form)


@OrderIC.route("/", methods=["POST"])
@login_required
@csrf.exempt
def index_post():
    """
     register a pcb order for user
    """
    ctx = {
        "orderICPage": "active"
    }
    form = OrderICForm()
    if not form.validate():
        flash("برخی موارد مقدار دهی نشده اند", "danger")
        return render_template("OrderIC/order.html", ctx=ctx, form=form)

    return "OK"




@OrderIC.route("/history/", methods=["GET"])
@login_required
def history_get():
    """user menu -> order printed ic history page"""
    ctx = {
        "orderICHistoryPage": "active"
    }
    return render_template("OrderIC/history.html", ctx=ctx)
