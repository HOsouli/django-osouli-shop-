from django import forms
from .models import PaymentType

# choice_PaymentTypes=(
#     (1, 'پرداخت از طریق درگاه بانکی'),
#     (2, 'پرداخت در محل')
#     )

from django import forms
from .models import PaymentType

class OrderForm(forms.Form):
    name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
        error_messages={'required': 'این فیلد نمیتواند خالی باشد'}
    )

    family = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
        error_messages={'required': 'این فیلد نمیتواند خالی باشد'}
    )

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
        required=False
    )

    phone_number = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل'}),
        required=False
    )

    address = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'آدرس', 'rows': '2'}),
        error_messages={'required': 'این فیلد نمیتواند خالی باشد'}
    )

    description = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'توضیحات', 'rows': '4'}),
        required=False
    )

    payment_type = forms.ModelChoiceField(
        queryset=PaymentType.objects.all(),
        empty_label=None,
        widget=forms.RadioSelect(),
        label=''
    )
