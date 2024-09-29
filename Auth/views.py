# build in

# current app
from . import auth
from . import form as AuthForm
from . import model as AuthModel
from . import utils as AuthUtils
from .Access import only_reset_password


# framework
from flask import (
    render_template,
    session,
    abort,
    url_for,
    redirect,
    flash,
    get_flashed_messages,
    request,
    current_app,
    make_response,
)

from sqlalchemy.exc import SQLAlchemyError

from Admin.model import Admin
from Config import Setting
from Core.email import sendActivAccounteMail, sendResetPasswordMail

# app
from Core.utils import get_next_page
from Core.extensions import db


@auth.get("/get/notifications/")
def get_notification():
    """Notification Messages view
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This view return user all flash messages in a json


    arguments:
        None -- clear

    return:
        return all flash messages in a json format


    - add no cacheing response of this view
    """
    flashes = []
    messages = get_flashed_messages(with_categories=True)

    for category, message in messages:
        temp = {"message": message, "category": category}
        flashes.append(temp)
    response = make_response(flashes)
    response.headers.add("Cache-Status", "disabled, saved-in-cdn-tracker, res,1,true")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@auth.route("/login/", methods=["GET"])
def login_get():
    """
    This View return login page for user
    """
    form = AuthForm.LoginForm()
    return render_template("login.html", form=form)


@auth.route("/login/", methods=["POST"])
def login_post():
    """
    this view take a post request for check user credential
    """
    next_page = get_next_page(fall_back_url=url_for("user.user_index"))
    form = AuthForm.LoginForm()
    if not form.validate():
        flash("برخی موارد مقداردهی نشده اند", "danger")
        return render_template("login.html", form=form)

    if not current_app.extensions["captcha3"].is_verify():
        flash("کپچا به درستی وارد نشده است", "danger")
        return redirect(next_page)

    username, password = form.Username.data, form.Password.data
    if not (user := AuthModel.User.query.filter_by(Username=username).first()):
        flash("کاربری با مشخصات وارد شده یافت نشد", "danger")
        return render_template("login.html", form=form)
    else:
        if not user.checkPassword(password):
            flash("اعتبارسنجی نادرست می باشد", "danger")
            return render_template("login.html", form=form)
        if not user.Active:
            flash("حساب کاربری مورد نظر فعال نمی باشد", "danger")
            return render_template("login.html", form=form)

        else:
            flash("کاربر گرامی خوش آمدید", "success")
            AuthUtils.login_user(user)

    return redirect(next_page)


@auth.route("/register/", methods=["GET"])
def register_get():
    """
    This View return Register template for user
    """
    form = AuthForm.RegisterForm()
    return render_template("register.html", form=form)


@auth.route("/register/", methods=["POST"])
def register_post():
    """
    this view take a post request that contain users information for register a new account
    """
    form = AuthForm.RegisterForm()
    if not form.validate():
        return render_template("register.html", form=form)

    if not current_app.extensions["captcha3"].is_verify():
        form.Submit.errors = ["کپچا به درستی وارد نشده است"]
        return render_template("register.html", form=form)

    User = AuthModel.User()
    if user := AuthModel.User.query.filter_by(
        Email=form.EmailAddress.data
    ).first():  # if user exists
        if user.Active:
            form.Submit.errors = ["آدرس ایمیل توسط کاربر دیگری گرفته شده است"]
            return render_template("register.html", form=form)
        else:
            # check if someone else is waiting for an email validation
            if AuthUtils.get_activation_email_slug_redis(
                key=form.EmailAddress.data
            ):  # if someone else is in line for activation
                form.EmailAddress.errors.append(
                    "لطفا دقایقی دیگر دوباره امتحان کنید ..."
                )
                form.EmailAddress.errors.append(
                    f"شما {AuthUtils.get_activation_ttl_slug_redis(form.EmailAddress.data)} دقیقه دیگر میتوانید اقدام به ساخت حساب کاربری کنید"
                )
                return render_template("register.html", form=form)
            else:
                # if someone else is not trying to activate this account delete one users from db
                try:
                    db.session.delete(user)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    current_app.logger.error(e)
                    flash("خطایی رخ داد, بعدا امتحان کنید", "danger")
                    return render_template("register.html", form=form)

    if not User.setUsername(form.Username.data):
        form.Username.errors = ["نام کاربری توسط کاربر دیگری گرفته شده است"]
        return render_template("register.html", form=form)

    if not User.setEmail(form.EmailAddress.data):
        form.EmailAddress.errors = ["آدرس ایمیل توسط کاربر دیگری گرفته شده است"]
        return render_template("register.html", form=form)

    User.SetPublicKey()
    User.setPassword(form.Password.data)
    try:
        db.session.add(User)
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        form.Submit.errors = ["خطایی رخ داد بعدا امتحان کنید"]
        return render_template("register.html", form=form)

    if not (
        token := AuthUtils.gen_and_set_activation_slug(email=form.EmailAddress.data)
    ):
        form.EmailAddress.errors = ["لطفا دقایقی دیگر دوباره امتحان کنید ..."]
        return render_template("register.html", form=form)

    sendActivAccounteMail(
        context={"token": token},
        recipients=[str(form.EmailAddress.data)],
        async_thread=False,  # not recommended
        async_celery=True,
    )
    return render_template("register.html", showSendActiveMail=True, form=form)


@auth.route("/Active/<string:token>/")
def active_account(token: str):
    """
    This View Activate User Account

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    this view take user unique activator key (uuid) and then validate
    that key and in the end activate user's account
    """

    resultEmail = AuthUtils.get_activation_token_slug_redis(token)
    if not resultEmail:
        abort(404)

    resultEmail = str(resultEmail)
    User = AuthModel.User.query.filter_by(Email=resultEmail).first_or_404()
    if User.Active:
        abort(404)
    else:

        # set users new language
        language = request.args.get(
            "language", "en"
        )  # get user language from args(GET)
        if language in current_app.config.get("LANGUAGES", list()):
            session["language"] = language

        User.Active = True
        try:
            db.session.add(User)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash("خطایی هنگام پردازش درخواست رخ داد. دوباره امتحان کنید", "success")
            return redirect(url_for("auth.login_get"))
        else:
            AuthUtils.delete_activation_token_slug_redis(token)  # delete token
            AuthUtils.delete_activation_email_slug_redis(User.Email)  # delete email
            flash("حساب کاربری با موفقیت فعال گردید", "success")
            flash("اکنون میتوانید وارد حساب کاربری خود شوید", "success")
            return redirect(url_for("auth.login_get"))


@auth.route("/forget_password/", methods=["GET"])
def forget_password_get():
    """
    this view return a  html page for users for Reset Password of  their accounts
    """
    ctx = {}
    form = AuthForm.ForgetPasswordForm()
    return render_template("forget_password.html", form=form, ctx=ctx)


@auth.route("/forget_password/", methods=["POST"])
def reset_password_post():
    """
    this view take a post request and check if users email is valid send a reset password to users mail account
    """

    ctx = {}
    form = AuthForm.ForgetPasswordForm()

    if not current_app.extensions["captcha3"].is_verify():
        flash("کپچا به درستی وارد نشده است", "danger")
        return render_template("forget_password.html", form=form, ctx=ctx)

    if not form.validate():
        return render_template("forget_password.html", form=form, ctx=ctx)

    if not (
        user := db.session.execute(
            db.select(AuthModel.User).filter_by(Email=form.EmailAddress.data)
        ).scalar_one_or_none()
    ):
        form.EmailAddress.errors.append("کاربری با آدرس ایمیل وارد شده یافت نشد")
        return render_template("forget_password.html", form=form, ctx=ctx)

    if (
        AuthUtils.get_reset_password_number(form.EmailAddress.data) >= 5
    ):  # limit 70 per week
        form.EmailAddress.errors.append("محدودیت ارسال ایمیل بازنشانی گذرواژه")
        form.EmailAddress.errors.append(
            "هر کاربر در هفته میتواند تنها 70 بار درخواست بازنشانی گذرواژه دهد"
        )
        return render_template("forget_password.html", form=form, ctx=ctx)

    last_reset_token = AuthUtils.get_reset_email_slug_redis(form.EmailAddress.data)
    if last_reset_token:
        AuthUtils.delete_reset_email_slug_redis(form.EmailAddress.data)
        AuthUtils.delete_reset_token_slug_redis(last_reset_token)

    if not (token := AuthUtils.gen_and_set_reset_slug(email=user.Email)):
        form.EmailAddress.errors.append("خطایی در هنگام درخواست رخ داد")
        return render_template("forget_password.html", form=form, ctx=ctx)

    sendResetPasswordMail(
        context={"token": token},
        recipients=[str(user.Email)],
        async_thread=False,  # not recommended but just for now !
        async_celery=True,
    )

    ctx["ResetPasswordMail"] = True
    return render_template("forget_password.html", form=form, ctx=ctx)


@auth.route("/check-reset-password/<string:token>", methods=["GET"])
def check_reset_password(token: str):
    """
    this view check reset password in url get params and if its valid
    redirect user to set password page
    """
    language = request.args.get("language", "en")  # get user language from args(GET)
    if language in current_app.config.get("LANGUAGES", list()):
        session["language"] = language

    if not (UserEmail := AuthUtils.get_reset_token_slug_redis(token)):
        abort(404)

    if not (UserToken := AuthUtils.get_reset_email_slug_redis(UserEmail)):
        abort(404)

    session["allow-set-password"] = True
    session["mail"] = UserEmail
    session["raw-token"] = UserToken
    return redirect(url_for("auth.set_password_get"))


@auth.route("/set-password/", methods=["GET"])
@only_reset_password
def set_password_get():
    """render setpassword for users that needs to be reset password"""
    form = AuthForm.SetNewPasswordForm()
    form.Token.data = session["raw-token"]
    return render_template("set_password.html", form=form)


@auth.route("/set-password/", methods=["POST"])
@only_reset_password
def set_password_post():
    form = AuthForm.SetNewPasswordForm()

    if not current_app.extensions["captcha3"].is_verify():
        flash("کپچا به درستی وارد نشده است", "danger")
        form.Submit.errors = ["کپچا به درستی وارد نشده است"]
        return render_template("set_password.html", form=form)

    if not form.validate():
        return render_template("set_password.html", form=form)

    if form.Token.data != session["raw-token"]:
        session.pop("allow-set-password")
        session.pop("mail")
        session.pop("raw-token")
        abort(404)

    if not (UserEmail := AuthUtils.get_reset_token_slug_redis(form.Token.data)):
        session.pop("allow-set-password")
        session.pop("mail")
        session.pop("raw-token")
        abort(404)

    if not (
        user := db.session.execute(
            db.select(AuthModel.User).filter_by(Email=UserEmail)
        ).scalar_one_or_none()
    ):
        session.pop("allow-set-password")
        session.pop("mail")
        session.pop("raw-token")
        abort(404)

    user.setPassword(form.Password.data)
    AuthUtils.delete_reset_token_slug_redis(form.Token.data)
    AuthUtils.delete_reset_email_slug_redis(UserEmail)
    AuthUtils.set_reset_password_number(email=session["mail"], value="0")

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.exception(exc_info=e)
        db.session.rollback()
        flash("خطایی رخ داد", "danger")
    else:
        flash("عملیات با موفقیت انجام شد", "success")

    session.pop("allow-set-password")
    session.pop("mail")
    session.pop("raw-token")

    return redirect(url_for("auth.login_get"))


@auth.route("/logout/", methods=["GET"])
def logout():
    """
    logout view
    """
    lang = session.get("language", "fa")
    session.clear()
    session["language"] = lang
    flash("با موفقیت از حساب کاربری خود خارج شدید", "success")
    return redirect(url_for("web.index_get"))


@auth.route(f"/admin/login/{Setting.ADMIN_LOGIN_TOKEN}/", methods=["GET"])
def admin_login_get():
    form = AuthForm.LoginForm()
    admin = Admin()
    admin.SetPublicKey()
    admin.setPassword("123654")
    admin.setUsername("admin")
    admin.setPhonenumber("09331016879")
    admin.setEmail("ali@ali.ir")
    admin.Active = True
    admin.save()
    return render_template("admin/admin-login.html", form=form)


@auth.route(f"/admin/login/{Setting.ADMIN_LOGIN_TOKEN}/", methods=["POST"])
def admin_login_post():
    """
    admin special login view
    """
    form = AuthForm.LoginForm()
    if not current_app.extensions["captcha3"].is_verify():
        flash("کپچا به درستی وارد نشده است", "danger")
        return render_template("admin/admin-login.html", form=form)

    if not form.validate():
        flash("برخی موارد به نظر گم شده اند", "danger")
        return render_template("admin/admin-login.html", form=form)

    admin: Admin = db.session.execute(
        db.select(Admin).filter_by(Username=form.Username.data)
    ).scalar_one_or_none()
    if not admin:  # check username
        flash("اعتبارسنجی ناموفق بود", "danger")
        return render_template("admin/admin-login.html", form=form)

    if not admin.checkPassword(form.Password.data):
        admin.TryNumber += 1
        admin.setLog(ip=request.real_ip, action="failed login")
        admin.save()
        return render_template("admin/admin-login.html", form=form)

    if not admin.canLogin():
        flash("حساب کاربری توسط سیستم به صورت خودکار قفل گردیده است", "danger")
        admin.TryNumber += 1
        admin.setLog(ip=request.real_ip, action="attempt to login/account locked")
        admin.save()
        return render_template("admin/admin-login.html", form=form)

    admin.TryNumber = 1
    admin.setLog(ip=request.real_ip, action="Successful login")
    admin.save()

    # this function login user to its account
    flash("ادمین گرامی خوش آمدید", "success")
    AuthUtils.login_admin(admin)

    return redirect(url_for("admin.index_get"))
