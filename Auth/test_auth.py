from flask import url_for


def test_login_page_is_ok(client, app):
    with app.app_context():
        response = client.get(url_for('auth.login_get'))
        assert response.status_code == 200
