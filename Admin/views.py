import os

from flask import current_app, send_from_directory, render_template
from . import admin
from .utils import admin_login_required



@admin.route("/AdminStatic/<path:filename>", methods=["GET"])
@admin_login_required
def Serve(filename):
    """
        Serve Static file only to admins that logged in to their account
    """
    static = current_app.config.get("BASE_DIR") / "Admin" / "private_static"
    if os.path.exists(os.path.join(static, filename)):
        return send_from_directory(static, filename)
    else:
        return "File Not Founded", 404


@admin.route("/", methods=["GET"])
@admin_login_required
def index_get():
    """admin index"""
    ctx = {
        "dashboard": "active"
    }
    return render_template("admin/index.html", ctx=ctx)
