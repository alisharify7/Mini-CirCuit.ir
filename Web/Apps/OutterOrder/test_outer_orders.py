from flask import url_for


def test_outer_order_page_is_ok(client, app):
    """testing outer_order page is return 200 ok and render template ok"""
    with app.app_context():
        response = client.get(url_for("web.outer_order.index_get"))
        assert response.status_code == 200
        assert "سفارش از خارج‌" in response.text
