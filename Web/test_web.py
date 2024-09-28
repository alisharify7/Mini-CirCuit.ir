from flask import url_for


def test_index_page_is_ok(client, app):
    """testing index page is return 200 ok and render template ok"""
    with app.app_context():
        response = client.get(url_for('web.index_get'))
        assert response.status_code == 200
        assert "فروش برد های الکترونیکی در ایران" in response.text




def test_about_us_page_is_ok(client, app):
    """testing about_us page is return 200 ok and render template ok"""
    with app.app_context():
        response = client.get(url_for('web.about_us_get'))
        assert response.status_code == 200
        assert "درباره ما" in response.text


def test_faq_page_is_ok(client, app):
    """testing faq  page is return 200 ok and render template ok"""
    # TODO: read faq from db
    with app.app_context():
        response = client.get(url_for('web.faq_get'))
        assert response.status_code == 200
        assert "سوالات متداول" in response.text


def test_contact_us_page_is_ok(client, app):
    """testing contact_us page is return 200 ok and render template ok"""
    with app.app_context():
        response = client.get(url_for('web.contact_us_get'))
        assert response.status_code == 200
        assert "ارتباط با ما" in response.text


def test_job_page_is_ok(client, app):
    """testing job_get page is return 200 ok and render template ok"""
    with app.app_context():
        response = client.get(url_for('web.job_get'))
        assert response.status_code == 200
        assert "فرصت های شغلی ما" in response.text


def test_proxy_page_is_ok(client, app):
    """testing proxy page is return 200 ok and render template ok"""
    with app.app_context():
        response = client.get(url_for('web.proxy_get'))
        assert response.status_code == 200
        assert "نمایندگان استانی" in response.text


def test_logo_page_is_ok(client, app):
    """testing logo page is return 200 ok and render template ok"""
    with app.app_context():
        response = client.get(url_for('web.logo_get'))
        assert response.status_code == 200
        assert "دانلود" in response.text
