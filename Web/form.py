from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length,Email as EmailValidator


class ValidateVarrantyForm(FlaskForm):
    """Login Users Form"""
    ProductNumber = StringField(
        validators=[
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=4,
                max=128,
                message='حداقل و حداکثر طول فیلد وارد شده باید 4-128 باشد'
            )

        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": "IB-MM-000000000000000000000",
            "dir": "ltr",
            "id": "ProductNumber"
        }
    )


    Submit = SubmitField(
        render_kw={
            "value": "اعتبار سنجی",
            "class": "btn bg-orange text-white w-100 py-2 my-3 fs-5 border-0",
            "id": "submitBtn"
        }
    )


class NewsLetterForm(FlaskForm):
    Email = EmailField(
        validators=[DataRequired(message="ورود داده در این فیلد الزامی می باشد"), InputRequired(message="ورود داده در این فیلد الزامی می باشد"), EmailValidator(message="ایمیل وارد شده نامعتبر می باشد")],
        render_kw={
            "class": "form-control rounded-0 rounded-start text-start",
            "placeholder": "آدرس ایمیل"
        }

    )
    Submit = SubmitField(
        render_kw={
            "value":"عضویت",
            "class":"btn bg-main-blue text-white input-group-text rounded-0 rounded-end"
        }
    )


class ContactUsForm(FlaskForm):
    Name = StringField(
        label="نام و نام خانوادگی",
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی می باشد"),
            InputRequired(message="ورود داده در این فیلد الزامی می باشد"),
            Length(min=1, max=256, message="حداقل و حداکثر طول فیلد 1-256 کارکتر می باشد")
         ],
        render_kw={
            "class": "form-control py-2 fs-5",
            "placeholder": "نام و نام خانوادگی به فارسی"
        }
    )

    Email = EmailField(
        label="آدرس ایمیل خود را وارد کنید",
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی می باشد"),
            InputRequired(message="ورود داده در این فیلد الزامی می باشد"),
            EmailValidator(message="ایمیل وارد شده نامعتبر می باشد"),
            Length(min=4, max=512, message="حداکثر و حداقل طول این فیلذ 4-512 کاراکتر می باشد")
        ],
        render_kw={
            "class": "text-start form-control py-2 fs-5",
            "placeholder": "example@gmail.com"
        }

    )

    Title = StringField(
        label="عنوان پیام خود را وارد کنید",
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی می باشد"),
            InputRequired(message="ورود داده در این فیلد الزامی می باشد"),
            Length(min=1, max=256, message="حداقل و حداکثر طول فیلد 1-256 کارکتر می باشد")
        ],
        render_kw={
            "class": "text-start form-control py-2 fs-5",
            "placeholder": "پیشنهاد, انتقاد, و ..."
        }

    )

    Message = TextAreaField(
        label="متن پیام خود را وارد کنید",
        validators=[
            DataRequired(message="ورود داده در این فیلد الزامی می باشد"),
            InputRequired(message="ورود داده در این فیلد الزامی می باشد"),
            Length(min=1, max=4096, message="حداقل و حداکثر طول فیلد 1-4096 کارکتر می باشد")
        ],
        render_kw={
            "class": "form-control py-2 fs-5 text-start",
            "placeholder": "پیشنهاد, انتقاد, و ...",
            "rows":"10"
        }
    )
    Submit = SubmitField(
        render_kw={
            "value":"ارسال",
            "class":"btn bg-blue w-100 fs-4 py-2 text-white"
        }
    )