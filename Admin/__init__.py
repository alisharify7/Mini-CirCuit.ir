from flask import Blueprint


admin = Blueprint(
    name="admin",
    import_name=__name__,
    static_folder="static/admin",
    template_folder="templates",
    static_url_path="adminPublicStatic",
)
from . import model, views


# register sub apps
from Admin.Apps.Users import admin_users

admin.register_blueprint(admin_users, url_prefix="/users/")

from Admin.Apps.Stencil import stencil

admin.register_blueprint(stencil, url_prefix="/stencil/")
