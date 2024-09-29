# framework
from flask import render_template, request, flash, redirect

# lib
from flask_babel import lazy_gettext as _l

import Core.utils as CoreUtils
import User.form as UserForm
from Auth.model import StenCilOrder
from Config import Setting

# apps
from Core.extensions import db
from User.utils import login_required
from . import OrderStencil


@OrderStencil.route("/", methods=["GET"])
@login_required
def index_get():
    """Users panel -> menu -> order stencil panel"""
    ctx = {"orderStencilPage": "active"}
    form = UserForm.StenCilOrderForm()
    return render_template("Orderstencil/order.html", ctx=ctx, form=form)


@OrderStencil.route("/", methods=["POST"])
@login_required
def index_post():
    """Order stencil for user"""
    ctx = {"orderStencilPage": "active"}
    form = UserForm.StenCilOrderForm()
    if not form.validate():
        flash(_l("برخی مقادیر به درستی ارسال نشده اند"), "danger")
        return render_template("Orderstencil/order.html", ctx=ctx, form=form)

    address = request.user_object.Address
    if not address:
        flash(
            _l(
                "آدرسی برای حساب کاربری شما ثبت نشده است ابتدا آدرس خود را در حساب کاربری خود کامل کنید"
            ),
            "danger",
        )
        return redirect(request.referrer)

    if not form.SIZE.data.startswith(form.TYPE.data):
        form.SIZE.errors.append(_l("سایز و نوع یکسان نمی باشد"))
        form.TYPE.errors.append(_l("سایز و نوع یکسان نمی باشد"))
        flash(_l("نوع و سایز درخواستی یکسان نمی باشد"), "danger")
        return render_template("Orderstencil/order.html", ctx=ctx, form=form)

    fileObj = request.files.get(form.FILE.short_name)
    if fileObj:
        fileName = CoreUtils.make_file_name_secure(fileObj.filename)
        fileObj.save(Setting.USERS_UPLOAD / fileName)
        form.FILE.data = fileName
    order = StenCilOrder()
    try:
        order.fill_from_form(form)
    except Exception as e:
        flash(e, "danger")
        return redirect(request.referrer)
    order.UserID = request.user_object.id
    order.Address = address
    order.SetPublicKey()

    if not order.save():
        flash(_l("خطایی هنگام پردازش درخواست رخ داد"), "danger")
        return render_template("Orderstencil/order.html", ctx=ctx, form=form)

    flash(_l("درخواست با موفقیت ثبت گردید"), "success")
    return redirect(request.referrer)


@OrderStencil.route("/history/", methods=["GET"])
@login_required
def history_get():
    ctx = {"OrderHistoryPage": "active"}
    page = request.args.get(key="page", default=1, type=int)
    records = db.paginate(
        select=db.select(StenCilOrder)
        .filter(StenCilOrder.UserID == request.user_object.id)
        .order_by(StenCilOrder.CreatedTime.desc()),
        per_page=10,
        page=page,
    )

    ctx["records"] = records
    ctx["current_page"] = page

    return render_template("Orderstencil/history.html", ctx=ctx)


@OrderStencil.route("/api/order/stencil/", methods=["GET"])
@login_required
def get_order_stencil_api():
    key = request.args.get(key="key", default="", type=str)

    if not key:
        return {"status": "failed", "message": "مقدار کد پیگیری یافت نشد"}, 400

    select = db.select(StenCilOrder).filter(StenCilOrder.PublicKey == key)
    stencil_db = db.session.execute(select).scalar_one_or_none()
    if not stencil_db:
        return {
            "status": "failed",
            "message": "رکوردی با کد پیگیری وارد شده یافت نشد",
        }, 400

    stencil_db.File = stencil_db.File if not stencil_db.File else stencil_db.File[33:]
    data = {
        "type": stencil_db.Type,
        "size": stencil_db.Size,
        "side": stencil_db.Side,
        "quantity": stencil_db.Quantity,
        "thickness": stencil_db.Thickness,
        "status": stencil_db.get_status(),
        "request": stencil_db.OtherRequest,
        "file": stencil_db.File,
        "address": stencil_db.Address,
        "identifier": key,
    }
    user = {
        "identifier": request.user_object.Email,
    }
    return {
        "status": "success",
        "data": data,
        "user": user,
        "x-token-tracker": True,
        "x-request-id": "http; x-request-id; set 1; done",
    }, 200
