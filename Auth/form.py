from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email


class FormFlask(FlaskForm):

    def validate_username(self):
        """
        Validate username contains valid characters

        username should be :
                all #english char
                with #igits
                and with #_

        """
        data = self.Username.data
        from string import ascii_lowercase, digits

        ascii_lowercase = [each for each in ascii_lowercase]
        digits = [each for each in digits]
        valid_char = [*digits, *ascii_lowercase]

        for each in data:
            if each not in valid_char:
                self.Username.errors = [
                    "فرمت ورودی اطلاعات نادرست است",
                    "فرمت درست اطلاعات شامل موارد زیر است",
                    "شامل اعداد و حروف انگلیسی",
                ]
                return False

        return True

    def validate(self):
        """Overwrite validate method for checking username"""
        if self.validate_username():
            return super().validate()
        else:
            return False


class LoginForm(FormFlask):
    """Login Users Form"""

    Username = StringField(
        validators=[
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=4,
                max=128,
                message="حداقل و حداکثر طول فیلد وارد شده باید 4-128 باشد",
            ),
        ],
        render_kw={"class": "form-control my-2 py-2", "placeholder": "نام کاربری"},
    )

    Password = PasswordField(
        validators=[
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=6,
                max=256,
                message=f"حداقل و حداکثر طول فیلد وارد شده باید 6-256 باشد",
            ),
        ],
        render_kw={"class": "form-control my-2 py-2", "placeholder": "گذرواژه"},
    )

    Submit = SubmitField(
        render_kw={
            "value": "ورود با گذرواژه",
            "class": "btn bg-main-blue text-white w-100 py-2 my-3 fs-5 border-0",
        }
    )


class RegisterForm(FormFlask):
    """Register Users Form"""

    Username = StringField(
        validators=[
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=4,
                max=128,
                message=f"داقل و حداکثر طول فیلد وارد شده باید 4-128 باشد",
            ),
        ],
        render_kw={"class": "form-control my-2 py-2", "placeholder": "نام کاربری"},
    )

    Password = PasswordField(
        validators=[
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=6,
                max=256,
                message=f"حداقل و حداکثر طول فیلد وارد شده باید 6-256 باشد",
            ),
        ],
        render_kw={"class": "form-control my-2 py-2", "placeholder": "گذرواژه"},
    )

    PasswordConfirm = PasswordField(
        validators=[
            EqualTo("Password", message="گذرواژه ها یکسان نمی باشد!"),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=6,
                max=256,
                message=f"حداقل و حداکثر طول فیلد وارد شده باید 6-256 باشد",
            ),
        ],
        render_kw={"class": "form-control my-2 py-2", "placeholder": "تکرار گذرواژه"},
    )

    EmailAddress = EmailField(
        validators=[
            Email(message=" آدرس ایمیل وارد شده نامعتبر می باشد "),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=4,
                max=256,
                message=f"حداقل و حداکثر طول فیلد وارد شده باید 11-256 باشد",
            ),
        ],
        render_kw={
            "class": "form-control my-2 py-2 text-start",
            "placeholder": "آدرس ایمیل",
        },
    )

    Submit = SubmitField(
        render_kw={
            "value": "ساخت حساب کاربری",
            "class": "btn bg-main-blue text-white w-100 py-2 my-3 fs-5 border-0",
        }
    )


class ForgetPasswordForm(FlaskForm):
    EmailAddress = EmailField(
        validators=[
            Email(message=" آدرس ایمیل وارد شده نامعتبر می باشد "),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=4,
                max=256,
                message=f"حداقل و حداکثر طول فیلد وارد شده باید 11-256 باشد",
            ),
        ],
        render_kw={
            "class": "form-control my-2 py-2 text-start",
            "placeholder": "آدرس ایمیل",
        },
    )

    Submit = SubmitField(
        render_kw={
            "value": "بازنشانی گذرواژه",
            "class": "btn bg-main-blue text-white w-100 py-2 my-3 fs-5 border-0",
        }
    )


class SetNewPasswordForm(FlaskForm):
    Password = PasswordField(
        validators=[
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=6,
                max=256,
                message=f"حداقل و حداکثر طول فیلد وارد شده باید 6-256 باشد",
            ),
        ],
        render_kw={
            "class": "form-control my-2 py-2",
            "placeholder": "گذرواژه",
        },
    )

    PasswordConfirm = PasswordField(
        validators=[
            EqualTo("Password", message="گذرواژه ها یکسان نمی باشد!"),
            DataRequired(message="وارد کردن داده در این فیلد الزامی است"),
            InputRequired(message="وارد کردن داده در این فیلد الزامی است"),
            Length(
                min=6,
                max=256,
                message=f"حداقل و حداکثر طول فیلد وارد شده باید 6-256 باشد",
            ),
        ],
        render_kw={"class": "form-control my-2 py-2", "placeholder": "تکرار گذرواژه"},
    )

    Token = HiddenField()
    Submit = SubmitField(
        render_kw={
            "value": "بازنشانی گذرواژه",
            "class": "btn bg-main-blue text-white w-100 py-2 my-3 fs-5 border-0",
        }
    )
