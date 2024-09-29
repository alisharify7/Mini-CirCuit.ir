from flask import render_template
from Admin.utils import admin_login_required
from . import stencil


@stencil.route("/", methods=["GET"])
def history_get():
    ctx = {}
    return render_template("history.html", ctx=ctx)
