from flask import render_template, request, flash, redirect

# app
from . import admin_users
from . import form as UserForm

# apps
from Core.extensions import db
from Auth.model import User
from Admin.utils import admin_login_required
from Core.email import sendActivAccounteMail
import Auth.utils as AuthUtils

# libs
import sqlalchemy as sa



@admin_users.route("/api/users/data/", methods=["GET"])
@admin_login_required
def api_get_users():
    # https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates

    query = db.session.query(User)
    search = request.args.get('search[value]')
    if search:
        query = query.filter(sa.or_(
            User.Username.like(f"{search}%"),
            User.FirstName.like(f"{search}%"),
            User.Email.like(f"{search}%"),
            User.LastName.like(f"{search}%"),
            User.PhoneNumber.like(f"{search}%"),
            User.Address.like(f"{search}%"),
        ))


    total_filtered = query.count()

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    Userquery = query.offset(start).limit(length)



    return {
        "data": [each.to_dict() for each in Userquery],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@admin_users.route("/", methods=["GET"])
@admin_login_required
def index_get():
    """return users page"""
    ctx = {
        "ManageUsersPage": "active"
    }
    return render_template("users.html", ctx=ctx)



@admin_users.route("/create/", methods=["GET"])
@admin_login_required
def create_new_user_get():
    """return create new user page"""
    ctx = {
        "createNewUser": "active"
    }
    form = UserForm.AddNewUserForm()
    return render_template("add-new-user.html", ctx=ctx, form=form)
@admin_users.route("/create/", methods=["POST"])
@admin_login_required
def create_new_user_post():
    """ create new user via post request"""
    ctx = {
        "createNewUser": "active"
    }
    form = UserForm.AddNewUserForm()
    if not form.validate():
        flash("خطایی رخ داد", "danger")
        return render_template("add-new-user.html", ctx=ctx, form=form)

    if form.validate():
        u = User()
        if (user := User.query.filter_by(Email=form.EmailAddress.data).first()):  # if user exists
            if user.Active: # if user wa
                form.Submit.errors = ['آدرس ایمیل توسط کاربر دیگری گرفته شده است']
                return render_template("add-new-user.html", ctx=ctx, form=form)
            else:
                if AuthUtils.get_activation_email_slug_redis(key=form.EmailAddress.data):  # if someone else is in line for activation
                    form.EmailAddress.errors.append("لطفا دقایقی دیگر دوباره امتحان کنید ...")
                    form.EmailAddress.errors.append("شما {} دقیقه دیگر میتوانید اقدام به ساخت حساب کاربری کنید".format(AuthUtils.get_activation_ttl_slug_redis(form.EmailAddress.data)))
                    return render_template("add-new-user.html", ctx=ctx, form=form)
                else:
                    try:
                        db.session.delete(user)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        flash("خطایی رخ داد", "danger")
                        return render_template("add-new-user.html", ctx=ctx, form=form)
        if not u.setUsername(form.Username.data):
            flash("نام کاربری تکراری می باشد", "danger")
            form.Username.errors = ["نام کاربری تکراری می باشد"]
            return render_template("add-new-user.html", ctx=ctx, form=form)

        if not u.setEmail(form.EmailAddress.data):
            flash("آدرس ایمیل تکراری می باشد", "danger")
            form.EmailAddress.errors = ["آدرس ایمیل تکراری می باشد"]
            return render_template("add-new-user.html", ctx=ctx, form=form)

        u.setPassword(form.Password.data)
        u.Active = form.Active.data == "active"
        u.SetPublicKey()
        if not u.save():
            flash("خطایی هنگام ذخیره کاربر رخ داد", "danger")
            return render_template("add-new-user.html", ctx=ctx, form=form)

        if not u.Active: # send activation mail
            if not (token := AuthUtils.gen_and_set_activation_slug(email=form.EmailAddress.data)):
                form.EmailAddress.errors = ["لطفا دقایقی دیگر دوباره امتحان کنید ..."]
                return render_template("add-new-user.html", ctx=ctx, form=form)

            sendActivAccounteMail(
                context={"token": token},
                recipients=[str(form.EmailAddress.data)],
                async_thread=False,  # not recommended
                async_celery=True,
            )
            flash("ایمیل تایید حساب کاربری با موفقیت برای ایمیل مورد نظر ارسال شد", "success")

        flash("عملیات با موفقیت انجام شد", "success")
        return redirect(request.referrer)
