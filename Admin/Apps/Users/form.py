from Auth.form import RegisterForm as AuthRegisterForm
from wtforms import SelectField


class AddNewUserForm(AuthRegisterForm):
    def __init__(self, *args, **kwargs):
        context = super().__init__(*args, **kwargs)

        delattr(self, "PasswordConfirm") # delete password confirm field

    Active = SelectField(
        choices=[("de-active", "غیرفعال-ایمیل تایید حساب کاربری ارسال کن"), ("active","فعال"), ],
        render_kw={
            "class": "form-control"
        }
    )

