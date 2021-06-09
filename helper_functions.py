from hashlib import sha256
import requests

SECRET_KEY = "SecretKey01"
PAYWAY = "advcash_rub"
SHOP_ID = 5


def my_pay(amount=None, shop_order_id=None):
    main_keys = {"shop_id": SHOP_ID,
                 "currency": 643,
                 "amount": float(amount),
                 "shop_order_id": shop_order_id}

    main_string = ':'.join(str(main_keys[x]) for x in sorted(main_keys)) + SECRET_KEY
    main_hash = sha256(main_string.encode('utf-8')).hexdigest()
    return main_hash


def my_invoice(amount=None, shop_order_id=None):
    main_keys = {
        "currency": "643",
        "payway": PAYWAY,
        "amount": amount,
        "shop_id": SHOP_ID,
        "shop_order_id": shop_order_id}

    main_string = ':'.join(str(main_keys[x]) for x in sorted(main_keys)) + SECRET_KEY
    main_hash = sha256(main_string.encode('utf-8')).hexdigest()

    data = {
        "currency": "643",
        "payway": PAYWAY,
        "amount": amount,
        "shop_id": SHOP_ID,
        "shop_order_id": shop_order_id,
        "sign": str(main_hash)
    }

    headers = {'Content-Type': 'application/json'}
    url = 'https://core.piastrix.com/invoice/create'
    # url2 = 'https://test-core.piastrix24.com/invoice/create'
    # url3 = 'https://polls.apiblueprint.org/invoice/try'
    # url4 = 'https://private-anon-a6d1ad090e-piastrix.apiary-mock.com/invoice/try'  # Mock server
    # url5 = 'https://polls.apiblueprint.org/invoice/create'

    reponse = requests.post(url, headers=headers, data=data)
    return reponse


def piastrix_request(amount=None, shop_order_id=None):
    main_keys = {
        "shop_id": SHOP_ID,
        "shop_currency": 840,
        "payer_currency": 840,
        "shop_amount": float(amount),
        "shop_order_id": shop_order_id}

    main_string = ':'.join(str(main_keys[x]) for x in sorted(main_keys)) + SECRET_KEY
    main_hash = sha256(main_string.encode('utf-8')).hexdigest()

    data = {
        "payer_currency": 840,
        "shop_amount": float(amount),
        "shop_currency": 840,
        "shop_id": SHOP_ID,
        "shop_order_id": shop_order_id,
        "sign": main_hash
    }
    headers = {'Content-Type': 'application/json'}

    url = "https://core.piastrix.com/bill/create"
    # url2 = 'https://polls.apiblueprint.org/bill/create'
    # url3 = 'https://private-anon-ec871f675f-piastrix.apiary-mock.com/bill/create'  # Mock server
    # url4 = 'https://private-anon-ec871f675f-piastrix.apiary-proxy.com/bill/create'

    reponse = requests.post(url, headers=headers, data=data)
    return reponse
