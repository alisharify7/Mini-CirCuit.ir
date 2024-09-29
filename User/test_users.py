import flask
from Auth.utils import login_user


def test_all_users_pages_required_login_auth(client, app):
    with app.app_context():
        # index page
        url = flask.url_for("user.user_index", _external=False)
        response = client.get(url)
        assert url in response.headers.get("Location", "")

        # send_ticket_get page
        url = flask.url_for("user.send_ticket_get", _external=False)
        response = client.get(url)
        assert url in response.headers.get("Location", "")

        # history_tickets_get page
        url = flask.url_for("user.history_tickets_get", _external=False)
        response = client.get(url)
        assert url in response.headers.get("Location", "")

        # setting_get page
        url = flask.url_for("user.setting_get", _external=False)
        response = client.get(url)
        assert url in response.headers.get("Location", "")


def test_all_users_pages_ok_with_login_credential(client, app):
    from Auth.form import LoginForm

    with app.app_context():
        with client:
            # login
            response = client.post(
                flask.url_for("auth.login_post"),
                data={"Username": app.user.Username, "Password": app.user.raw_password},
            )
            assert response.status_code == 301
            # index page
            url = flask.url_for("user.user_index", _external=False)
            response = client.get(url)
            assert url in response.headers.get("Location", "")

            # send_ticket_get page
            url = flask.url_for("user.send_ticket_get", _external=False)
            response = client.get(url)
            assert url in response.headers.get("Location", "")

            # history_tickets_get page
            url = flask.url_for("user.history_tickets_get", _external=False)
            response = client.get(url)
            assert url in response.headers.get("Location", "")

            # setting_get page
            url = flask.url_for("user.setting_get", _external=False)
            response = client.get(url)
            assert url in response.headers.get("Location", "")
