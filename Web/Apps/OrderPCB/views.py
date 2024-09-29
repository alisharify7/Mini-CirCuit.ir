from flask import render_template

from . import blp
from . import form as OrderPCBForm

from Core.extensions import csrf


@blp.route("/", methods=["GET"])
def pcb_get():
    """
    this View return proxy state page
    """
    return render_template("pcb.html")


@blp.route("/calculator//", methods=["GET"])
def calculator_get():
    """
    this View return proxy state page
    """
    form = OrderPCBForm.OrderICForm()
    return render_template("calculator.html", form=form)


@blp.route("/calculator/", methods=["POST"])
@csrf.exempt
def calculator_post():
    """
    this View return proxy state page
    """
    form = OrderPCBForm.OrderICForm()
    if not form.validate():
        return {"status": "failed", "message": form.errors}, 400

    price, day, message = form.calculate_price()
    data = {"price": price, "day": day, **form.data, "message": message}
    return data, 200
