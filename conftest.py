import pytest
from Core import create_app
from Core.extensions import db
from Auth.model import User
from Config import Setting

@pytest.fixture()
def app():
    """ Flask Main Application """
    setting = Setting()
    setting.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" # switch to memory
    setting.TESTING = True
    setting.SERVER_NAME = "localhost:5000"
    setting.GOOGLE_CAPTCHA_V2_CONF["CAPTCHA_ENABLED"] = False
    setting.GOOGLE_CAPTCHA_V3_CONF["CAPTCHA_ENABLED"] = False

    app = create_app(setting)


    def getUser():
        if (u := User.query.filter_by(Email="test_user@user.com").first()):
            return u
        u = User()
        u.Email = "test_user@user.com"
        u.Username = "test_user"
        u.setPassword("password")
        u.Active = True
        with app.app_context():
            u.SetPublicKey()
            u.save()
        u.raw_password = "password"
        return u

    with app.app_context():
        db.create_all()
        app.user = getUser()

    yield app


@pytest.fixture()
def client(app):
    """ Simple client for testing Flask application """
    yield app.test_client()
