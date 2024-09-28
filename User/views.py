# build in
import os

# current app
from . import user
from . import form as UserForm


# framework
from flask import (render_template, send_from_directory, request,
                   flash, redirect, current_app, session, url_for)

# app.project
from Core.extensions import db
from Auth.model import Ticket
from Auth.Access import login_required
from Core.utils import make_file_name_secure
from Core.template_filter import StorageUrl

# libs
from lib.file import get_file_size


@user.route("/UserStatic/<path:filename>", methods=["GET"])
@login_required
def Serve(filename):
    """
        Serve Static file only to users that logged in to their account
    """
    static = current_app.config.get("BASE_DIR") / "User" / "private_static"
    if os.path.exists(os.path.join(static, filename)):
        return send_from_directory(static, filename)
    else:
        return "File Not Founded", 404


@user.route("/", methods=["GET"])
@login_required
def user_index():
    """return users index dashboard panel """
    ctx = {
        "dashboard": "active"
    }
    return render_template("user/index.html", ctx=ctx)


@user.route("/send-ticket/", methods=["GET"])
@login_required
def send_ticket_get():
    """return send ticket page for users """
    ctx = {
        "send_ticket": "active"
    }
    form = UserForm.TicketForm()
    attachment_ext = current_app.config.get("TICKET_ATTACHMENT_EXT", ["zip"])

    form.File.render_kw.update({"accept": ",".join([f".{_}" for _ in attachment_ext])})
    form.File.ext = form.File.render_kw["accept"]
    return render_template("user/send-ticket.html", ctx=ctx, form=form)


@user.route("/send-ticket/", methods=["POST"])
@login_required
def send_ticket_post():
    """send a ticket to support -> post"""
    ctx = {
        "send_ticket": "active"
    }

    form = UserForm.TicketForm()
    if not form.validate():
        flash('برخی موارد به درستی وارد نشده است', "danger")
        current_app.logger.info(
            msg=f"\nError for User: {request.user_object.getName(True)}\nForm Validate Error.\n\t{form.errors}\n")
        return render_template("user/send-ticket.html", ctx=ctx, form=form)

    ticket = Ticket()
    ticket.Title = form.Title.data
    ticket.Caption = form.Caption.data
    ticket.SetPublicKey()
    ticket.setUserID(request.user_object)

    attachment_ext = current_app.config.get("TICKET_ATTACHMENT_EXT", ["zip"])



    if (file := request.files.get(form.File.name)):

        if get_file_size(file) > current_app.config.get("TICKET_ATTACHMENT_MAX_SIZE", 1024*1024*16):
            flash("حجم فایل ارسالی بیشتر از حد تایین شده می باشد", "danger")
            flash("حداکثر حجم فایل ارسالی 16MB می باشد", "danger")
            return render_template("user/send-ticket.html", ctx=ctx, form=form)

        if ("." in file.filename):
            f = file.filename.split(".")[-1]
            if f not in attachment_ext:
                flash("پسوند فایل ارسالی پشتیبانی نمی شود", "danger")
                return render_template("user/send-ticket.html", ctx=ctx, form=form)

        else:
            flash("نام فایل نامعتبر می باشد", "danger")
            return render_template("user/send-ticket.html", ctx=ctx, form=form)

        file.filename = make_file_name_secure(file.filename)
        file_path = current_app.config.get("TICKET_ATTACHMENT_DIR", "STORAGE_DIR") / file.filename
        file.save(file_path)
        ticket.File = file.filename

    if not ticket.save():
        # delete file
        if os.path.exists(file_path):
            os.remove(file_path)

        flash("خطایی رخ داد!", "danger")
        return redirect(url_for('user.send_ticket_get'))
    else:
        flash("عملیات با موفقیت انجام شد", "success")
        return redirect(url_for('user.history_tickets_get'))


@user.route("/history-ticket/", methods=["GET"])
@login_required
def history_tickets_get():
    """return all ticket history"""
    ctx = {
        "history_ticket": "active"
    }

    page = request.args.get(key="page", default=1, type=int)
    ctx["tickets"] = db.paginate(max_per_page=15, per_page=10, page=page,
                                 select=db.select(Ticket) \
                                 .filter(Ticket.UserID == request.user_object.id) \
                                 .order_by(Ticket.CreatedTime.desc()))
    ctx["current_page"] = page
    return render_template("user/history-tickets.html", ctx=ctx)


@user.route("/ticket-info/", methods=["POST"])
@login_required
def ticket_info_post():
    """[API-view] return a ticket info """
    ctx = {}
    ticketID = request.form.get("TICKET_ID", None) # TICKET_ID -> ticket.PublicKey
    if not ticketID:
        return {"status": "failed", "message": "برخی مقادیر به نظر گم شده اند!" + "TICKET_ID:string:missing"}, 400

    query = db.select(Ticket) \
        .filter_by(PublicKey=ticketID) \
        .filter_by(UserID=request.user_object.id)

    ticket = db.session.execute(query).scalar_one_or_none()
    if not ticket:
        return {"status": "failed", "message":"تیکتی با شماره وارد شده یافت نشد"}, 404


    data = {
        "ticket_number": ticket.id,
        "title": ticket.Title,
        "message": ticket.Caption,
        "created_at": ticket.ConvertToJalali(obj_time=ticket.CreatedTime, full_time=True), #TODO: use Moment js instead
        "answer": ticket.Answer or None,
        "answer_error": "پاسخی به تیکت مورد نظر داده نشده است",
        "attachment": StorageUrl("TicketAttachment/"+ ticket.File) if ticket.File else None
    }

    return {"status": "success", "message": data}, 200


@user.route("/setting/", methods=["GET"])
@login_required
def setting_get():
    """return setting page for users"""
    ctx = {
        "setting": "active"
    }

    form = UserForm.Setting()

    form.Username.data = request.user_object.Username
    form.FirstName.data = request.user_object.FirstName or None
    form.LastName.data = request.user_object.LastName or None
    form.Email.data = request.user_object.Email or None
    form.Address.data = request.user_object.Address or None
    form.PhoneNumber.data = request.user_object.PhoneNumber or None

    return render_template("user/setting.html", ctx=ctx, form=form)


@user.route("/setting/", methods=["POST"])
@login_required
def setting_post():
    """update setting for users -> POST"""
    ctx = {
        "setting": "active"
    }

    form = UserForm.Setting()
    if not form.validate():
        flash("برخی مقادیر مقدار دهی نشده اند", "danger")
        return render_template("user/setting.html", ctx=ctx, form=form)

    user = request.user_object
    if form.Password.data:
        if len(form.Password.data) >= 6: # TODO: use validate decorator in db layer
            user.setPassword(form.Password.data)
        else:
            form.Password.errors.append("حداقل طول گذرواژه باید 6 کاراکتر باشد")
            return render_template("user/setting.html", ctx=ctx, form=form)

    if form.Username.data and not (form.Username.data == user.Username):
        if not user.setUsername(form.Username.data):
            form.Username.errors.append("نام کاربری توسط کاربر دیگری گرفته شده است")
            return render_template("user/setting.html", ctx=ctx, form=form)

    if form.Address.data:
        user.Address = form.Address.data

    if form.Email.data and not (form.Email.data == user.Email):
        if not user.setEmail(form.Email.data):
            form.Email.errors.append("آدرس ایمیل توسط کاربر دیگری گرفته شده است")
            return render_template("user/setting.html", ctx=ctx, form=form)

    if form.PhoneNumber.data and not (form.PhoneNumber.data == user.PhoneNumber):
        if not user.setPhonenumber(form.PhoneNumber.data):
            form.PhoneNumber.errors.append("شماره تلفن همراه توسط کاربر دیگری گرفته شده است")
            return render_template("user/setting.html", ctx=ctx, form=form)

    user.FirstName = form.FirstName.data
    user.LastName = form.LastName.data

    if not user.save():
        flash("خطایی رخ داد بعدا امتحان کنید", "danger")
    else:
        session["password"] = user.Password # update hash password in session
        flash("عملیات با موفقیت انجام شد", "success")

    return redirect(url_for('user.setting_get'))


