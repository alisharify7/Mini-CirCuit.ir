from . import payment

from idpay.api import IDPayAPI

idpay = IDPayAPI(
    api_key="67b5830d-56ce-45d0-a9f9-d3dcdb6377c9",
    sandbox=True,
    domain="http://localhost:8000",
)

@payment.get("/")
def payment(request):
    payer = {
        "name": "علی شریفی",
        "mail": "alisharifyofficial@gmail.com",
        "phone":"09331016879",
        "desc": "تست توضیحات"
    }
    x = idpay.payment(
        order_id="5565565x565c",
        payer=payer,
        amount=100000,
        callback_page="/payment/callback",
    )