from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, StringField, SubmitField, IntegerField
from wtforms.validators import Length, DataRequired, InputRequired, NumberRange


class RegisterOrderAboardForm(FlaskForm):

    Name = StringField(
        label="نام محصول",
        validators=[
            Length(min=1, max=512, message="حداقل و حداکثر طول این فیلد 1-512 کاراکتر است"),
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "class": "form-control mb-3",
            "placeholder": "مثال ps4 slim 256g مشکی",
        }
    )
    Quantity = IntegerField(
        label="تعداد محصول",
        validators=[
            NumberRange(min=1, max=10000, message="حداقل تعداد سفارش 1 و حداکثر 10000 سفارش می باشد"),
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "class": "form-control mb-3",
            "placeholder": "10",
        }
    )
    Link = StringField(
        label="لینک محصول",
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "https://amazom.com/buy/example لینک محصول",
        }
    )

    Description = TextAreaField(
        label="توضیحات اضافی",
        validators=[
            Length(min=1, max=4096, message="حداقل و حداکثر تعداد ورودی در این فرم 1-4096 کاراکتر می باشد"),
            DataRequired(message="ورود داده در این فیلد الزامی است"),
            InputRequired(message="ورود داده در این فیلد الزامی است")
        ],
        render_kw={
            "class": "form-control mb-3",
            "placeholder": "سایر توضیحات / رنگ, سایز, ...",
            "rows" : "15"
        }
    )

    File = FileField(
        validators=[],
        render_kw={
            "class": "form-control mb-3",
            "placeholder": "فایل",
        }
    )

    Submit = SubmitField(
        render_kw={
            "class":"btn btn-primary w-100 fs-5",
            "value":"ثبت سفارش"
        }
    )