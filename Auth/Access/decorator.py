# build in
from functools import wraps

# framework
from flask import session, request, redirect, url_for, flash, abort

# lib

# app
from Auth.model import User


# TODO: remote this decorator and use login_manager decorator
def login_required(f):
    """Base Login required Decorator for users"""

    @wraps(f)
    def inner(*args, **kwargs):
        next = request.url_rule

        # check user login
        message = "برای دسترسی به صفحه مورد نیاز ابتدا وارد حساب کاربری خود شوید"
        if not session.get("login", False):
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # get user id
        if not session.get("account-id"):
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # check user id
        try:
            user = User.query.get(session.get("account-id"))
            if not user:
                raise ValueError
        except Exception as e:
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # check password
        if user.Password != (session.get("password")):
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        if not user.Active:
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        return f(*args, **kwargs)

    return inner


def only_reset_password(f):
    """Only reset password users """

    @wraps(f)
    def inner(*args, **kwargs):

        if not session.get("mail", False):
            abort(404)

        # get user id
        if not session.get("allow-set-password"):
            abort(404)

        return f(*args, **kwargs)

    return inner

def admin_login_required(f):
    """Base Login required Decorator for admins"""
    from Admin.model import Admin

    @wraps(f)
    def inner(*args, **kwargs):
        next = request.url_rule

        # check user login
        message = "برای دسترسی به صفحه مورد نیاز ابتدا وارد حساب کاربری خود شوید"
        if not session.get("login", False):
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # get user id
        if not session.get("account-id"):
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # check user id
        try:
            admin = Admin.query.get(session.get("account-id"))
            if not admin:
                raise ValueError
        except Exception as e:
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        # check password
        if admin.Password != (session.get("password")):
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        if not admin.Active:
            flash(message, "danger")
            return redirect(url_for("auth.login_get", next=next))

        return f(*args, **kwargs)

    return inner