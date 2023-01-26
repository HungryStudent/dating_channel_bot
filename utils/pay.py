from yoomoney import Quickpay

from config import yoomoney_id, price


def get_pay_url(profile_id, days):
    quickpay = Quickpay(
        receiver=yoomoney_id,
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=price[days],
        label=profile_id
    )
    return quickpay.redirected_url
