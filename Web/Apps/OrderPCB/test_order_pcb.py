from flask import url_for


def test_pcb_page_is_ok(client, app):
    """testing index page is return 200 ok and render template ok"""
    with app.app_context():
        response = client.get(url_for("web.orderPCB.pcb_get"))
        assert response.status_code == 200
        assert "PCB سفارش  برد مدارچاپی" in response.text


def test_pcb_calculator_page_is_ok(client, app):
    """testing outer_order page is return 200 ok and render template ok"""
    with app.app_context():
        response = client.get(url_for("web.orderPCB.calculator_get"))
        assert response.status_code == 200
        assert "محاسبه آنلاین قیمت برد مدارچاپی" in response.text
