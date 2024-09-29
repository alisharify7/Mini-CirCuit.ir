# build in


# libs
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    EmailField,
    SelectField,
    SelectMultipleField,
    IntegerField,
    FileField,
)
from wtforms.validators import (
    Length,
    DataRequired,
    InputRequired,
    Email as EmailValidator,
    Regexp,
    NumberRange,
)
from wtforms.widgets import ListWidget, CheckboxInput

# apps
from Auth.model import StenCilOrder


class CheckBoxField(SelectMultipleField):
    """Check Box Form"""

    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class TicketForm(FlaskForm):
    """
    Sending a Ticket Html Form
    """

    Title = StringField(
        label="عنوان تیکت",
        validators=[
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=6,
                max=64,
                message=f"حداقل و حداکثر طول داده در این فیلد 6-64 می باشد",
            ),
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": "مشکل مالی - درخواست سفارش - پیشنهاد, انتقاد",
        },
    )

    Caption = TextAreaField(
        label="توضیحات",
        validators=[
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=6,
                max=512,
                message=f"حداقل و حداکثر طول داده در این فیلد 6-512 می باشد",
            ),
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": "توضیحاتی مرتبط با عنوان تیکت",
            "rows": "10",
            "cols": "10",
        },
    )

    File = FileField(validators=[], render_kw={"class": "form-control"})

    Submit = SubmitField(
        render_kw={
            "value": "ثبت",
            "class": "btn bg-primary text-white w-100 py-2 my-3 fs-5 border-0 fs-4",
        }
    )


class Setting(FlaskForm):
    """
    Sending a Ticket Html Form
    """

    FirstName = StringField(
        validators=[],
        render_kw={"class": "form-control my-2 py-2 fs-5", "placeholder": "نام"},
    )

    LastName = StringField(
        validators=[],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": "نام خانوادگی",
        },
    )
    Username = StringField(
        validators=[
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=5,
                max=128,
                message=f"حداقل و حداکثر طول داده در این فیلد 6-64 می باشد",
            ),
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": "نام کاربری",
        },
    )
    Password = PasswordField(
        validators=[],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": "گذرواژه",
        },
    )

    Email = EmailField(
        validators=[
            EmailValidator(message="ایمیل وارد شده نامعتبر می باشد"),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": "آدرس ایمیل",
        },
    )

    Address = TextAreaField(
        validators=[],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": "آدرس منزل",
            "rows": 10,
            "cols": 20,
        },
    )
    PhoneNumber = StringField(
        validators=[
            Regexp(
                regex=r"^((0|0098|\+98)?9\d{9})?$",
                message="فرمت وارد شده برای تلفن نامعتبر می باشد",
            ),
        ],
        render_kw={
            "class": "form-control my-2 py-2 fs-5",
            "placeholder": "شماره تلفن همراه",
        },
    )

    Submit = SubmitField(
        render_kw={
            "value": "بروزرسانی",
            "class": "btn bg-primary text-white w-100 py-2 my-3 fs-5 border-0 fs-4",
        }
    )


class StenCilOrderForm(FlaskForm):
    def __init__(self):
        content = super().__init__()

        types = StenCilOrder.StenCilTypes
        self.TYPE.choices = [(each.value, each.value) for each in types]

        sizes = StenCilOrder.StenCilSizes
        self.SIZE.choices = [(each.value, each.value) for each in sizes]

        sides = StenCilOrder.StenCilSides
        self.SIDE.choices = [(each.value, each.value) for each in sides]

        thickness = StenCilOrder.StenCilThickness
        self.THICKNESS.choices = [(each.value, each.value) for each in thickness]

        faducials = StenCilOrder.StenCilFiducials
        self.FIDUCIALS.choices = [(each.value, each.value) for each in faducials]

        return content

    TYPE = SelectField(
        label="Stencil Type",
        choices=list(),
        validators=[DataRequired(), InputRequired()],
        render_kw={"class": "form-control", "placeholder": "stencil type"},
    )

    SIZE = SelectField(
        label="Stencil Size",
        choices=list(),
        validators=[DataRequired(), InputRequired()],
        render_kw={"class": "form-control", "placeholder": "stencil Size"},
    )

    SIDE = SelectField(
        label="Stencil Side",
        choices=list(),
        validators=[DataRequired(), InputRequired()],
        render_kw={"class": "form-control", "placeholder": "slide "},
    )

    QUANTITY = IntegerField(
        label="Stencil Quantity",
        validators=[DataRequired(), InputRequired(), NumberRange(min=0, max=10000)],
        render_kw={"class": "form-control", "placeholder": "0 "},
    )

    THICKNESS = SelectField(
        label="Stencil THICKNESS",
        validators=[DataRequired(), InputRequired()],
        render_kw={"class": "form-control", "placeholder": "THICKNESS "},
    )

    FIDUCIALS = SelectField(
        label="Stencil FIDUCIALS",
        validators=[
            DataRequired(),
            InputRequired(),
        ],
        render_kw={"class": "form-control", "placeholder": "FIDUCIALS "},
    )

    REQUEST = TextAreaField(
        label="request",
        validators=[],
        render_kw={
            "class": "form-control",
            "placeholder": "optional, description",
            "rows": "5",
        },
    )

    FILE = FileField(label="file", validators=[], render_kw={"class": "form-control"})

    SUBMIT = SubmitField(
        render_kw={"class": "w-100 my-2 btn btn-primary", "value": "ثبت سفارش"}
    )
