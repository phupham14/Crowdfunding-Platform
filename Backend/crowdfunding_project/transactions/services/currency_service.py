# transactions/services/currency_service.py

def vnd_to_usd(vnd_amount: int) -> int:
    rate = 26000  # 1 USD ≈ 26,000 VND (dev)
    usd = vnd_amount / rate
    return int(usd * 100)  # Stripe cần cent


def usd_to_vnd(usd_amount: float) -> int:
    rate = 26000  # 1 USD ≈ 26,000 VND (dev)
    return int(usd_amount * rate)