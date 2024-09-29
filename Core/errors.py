# app
from . import app

# framework
from flask import render_template

errors = {
    "404": {
        "title": "یافت نشد!",
        "code": 404,
        "caption": "صفحه ای مورد نظر یافت نشد",
        "image": "media/errors/404.svg",
    },
    "500": {
        "title": "خطایی رخ داد",
        "code": 500,
        "caption": "خطایی حین پردازش درخواست رخ داد/ ما اطلاعات درخواست را برای تیم پشتیبانی ارسال کردیم\n لطفا دقایقی دیگر دوباره امتحان کنید",
        "image": "media/errors/500.svg",
    },
    "400": {
        "title": "درخواست به درستی ارسال نشد",
        "code": 400,
        "caption": "خطایی حین پردازش درخواست رخ داد/ ما اطلاعات درخواست را برای تیم پشتیبانی ارسال کردیم\n لطفا دقایقی دیگر دوباره امتحان کنید",
        "image": "media/errors/500.svg",
    },
}


@app.errorhandler(404)
def error_404(e) -> str:
    """error 404 page"""
    ctx = errors["404"]
    return render_template("errors/error-page.html", ctx=ctx), 404


@app.errorhandler(500)
def error_500(e) -> str:
    """error 500 page"""
    ctx = errors["500"]
    return render_template("errors/error-page.html", ctx=ctx), 500


# @app.errorhandler(400)
# def error_400(e) -> str:
#     """error 400 page"""
#     ctx = errors["400"]
#     return render_template("errors/error-page.html", ctx=ctx), 400
