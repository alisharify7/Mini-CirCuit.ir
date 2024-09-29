from flask import Blueprint

admin_users = Blueprint(
    "users",
    __name__,
    template_folder="templates/admin-sub-users",
)

from . import views
