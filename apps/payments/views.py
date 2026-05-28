from django.shortcuts import render,redirect,redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order
from .models import Payment
from apps.accounts.models import Customer
from django.conf import settings
import requests
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/payments/verify/'

# ____________________________________________________________
class ZarinpalPaymentView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            order = get_object_or_404(Order, id=order_id, customer__user=request.user)

            amount = int(order.get_order_total_price() * 10)
            if amount <= 0:
                return HttpResponse("مبلغ سفارش معتبر نیست!")

            customer = Customer.objects.get(user=request.user)

            payment = Payment.objects.create(
                order=order,
                customer=customer,
                amount=amount,
                description="پرداخت از طریق درگاه زرین پال"
            )

            request.session['payment_session'] = {
                'order_id': order.id,
                'payment_id': payment.id
            }

            metadata = {}
            if customer.phone_number:
                metadata['mobile'] = str(customer.phone_number)
            if request.user.email:
                metadata['email'] = str(request.user.email)

            # Debug print
            print(f"Metadata sent to Zarinpal: {metadata}")

            req_data = {
                "merchant_id": settings.ZARINPAL_MERCHANT_ID,
                "amount": amount,
                "description": "پرداخت سفارش",
                "callback_url": CallbackURL,
                "metadata": metadata
            }

            response = requests.post(
                ZP_API_REQUEST,
                json=req_data,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                timeout=10
            )

            response_json = response.json()

            if response_json.get('errors'):
                return HttpResponse(f"<pre>خطای زرین‌پال:\n{response_json['errors']}</pre>")

            data = response_json.get('data')
            if not data:
                return HttpResponse(f"<pre>پاسخ نامعتبر از زرین‌پال:\n{response_json}</pre>")

            authority = data.get('authority')
            if not authority:
                return HttpResponse(f"<pre>authority دریافت نشد:\n{response_json}</pre>")

            return redirect(ZP_API_STARTPAY + authority)

        except Exception as e:
            return HttpResponse(f"خطای سرور: {str(e)}")

# _________________________________________________________________
class ZarinpalPaymentVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        Status = request.GET.get('Status')
        if Status != 'OK':
            return redirect("payments:show_verify_message", message=" خطا در پرداخت")

        try:
            session_data = request.session.get('payment_session')
            order = Order.objects.get(id=session_data['order_id'])
            payment = Payment.objects.get(id=session_data['payment_id'])

            authority = request.GET.get('Authority')
            req_data = {
                "merchant_id": settings.ZARINPAL_MERCHANT_ID,
                "authority": authority,
                "amount": int(order.get_order_total_price() * 10)
            }

            #  v4 API
            response = requests.post(
                ZP_API_VERIFY,
                json=req_data,
                headers={"Content-Type": "application/json"}
            )

            response_json = response.json()
            if response_json.get('errors'):
                return redirect("payments:show_verify_message", f" {response_json['errors']}")

            data = response_json['data']
            code = data['code']
            ref_id = data['ref_id']
            order.is_finally = True
            order.save()
            payment.is_finally = True
            payment.status_code = code
            payment.ref_id = str(ref_id)
            payment.save()

            request.session.pop('payment_session', None)

            msg = f" موفق! رهگیری: {ref_id}" if code == 100 else f" قبلاً: {ref_id}"
            return redirect("payments:show_verify_message", message=msg)

        except Exception as e:
            return redirect("payments:show_verify_message", f" {str(e)}")

# _________________________________________________________________
#  تابع نمایش دادن بعد از پرداخت نهایی تو زرین پال که پیام موفقیت آمیز رو نشون میده
def show_verify_message(request,message):
    return render(request, 'payments_app/verify_message.html', {'message':message})
