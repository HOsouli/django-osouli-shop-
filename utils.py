import os
import secrets
import string
import requests
import json
from django.conf import settings
from decimal import Decimal

# __________________________________________________________________________
def generate_activation_code(length=6):
    characters = string.digits
    code = ''.join(secrets.choice(characters) for _ in range(length))
    return code

# __________________________________________________________________________
def send_sms_ir(mobile, code):
    mobile = mobile.strip()

    # Normalize Mobile
    mobile = mobile.strip()
    if mobile.startswith("09"):
        mobile = "98" + mobile[1:]
    elif mobile.startswith("+98"):
        mobile = mobile[1:]

    url = "https://api.sms.ir/v1/send/verify"

    payload = {
        "mobile": mobile,
        "templateId": int(settings.SMS_IR_VERIFY_TEMPLATE_ID),
        "parameters": [
            {
                "name": "Code",
                "value": str(code)
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/plain",
        "x-api-key": settings.SMS_IR_API_KEY,
        # "x-api-key": api_key,
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=20)

        print("==== SMS.IR VERIFY REQUEST ====")
        print("URL:", url)
        print("HEADERS:", headers)
        print("PAYLOAD:", payload)

        print("==== SMS.IR VERIFY RESPONSE ====")
        print("STATUS:", r.status_code)
        print("BODY:", r.text)

        if r.status_code == 200:
            data = r.json()
            return data.get("status") == 1

        return False

    except requests.RequestException as e:
        print("VERIFY SMS ERROR:", str(e))
        return False


# __________________________________________________________________________
def send_activation_sms(mobile, code):
    result = send_sms_ir(mobile, code)

    return True if result else False

# __________________________________________________________________________
from uuid import uuid4

class FileUpload:
    def __init__(self, dir, prefix):   # پوشه ای که مربوط به برند prefix
        self.dir = dir
        self.prefix = prefix

    def upload_to(self, instance, filename):
        filename, ext = os.path.splitext(filename)    # a.jpg ==>        a=>filename,   jpg=>ext
        return f'{self.dir}/{self.prefix}/{uuid4()}{ext}'

# __________________________________________________________________________
# این تابع قیمت رو میگیره و تخفیف هم پیشفرض 0 میده که اگر تخفیف نداشت صفر حساب میکنه
def price_by_delivery_tax(price, discount=0):
    price = Decimal(price)
    delivery = Decimal('250000')
    if price > Decimal('2000000'):
        delivery = Decimal('0')
    tax_rate = Decimal('0.09')
    discount_rate = Decimal(str(discount)) / Decimal('100')
    tax = (price + delivery) * tax_rate
    subtotal = price + delivery + tax
    final_price = subtotal - (subtotal * discount_rate)

    return int(final_price), int(delivery), int(tax)





