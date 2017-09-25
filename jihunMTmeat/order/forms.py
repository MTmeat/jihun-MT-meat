from django import forms
from datetimewidget.widgets import DateTimeWidget

from order.models import Orderer, Order


class OrdererForm(forms.ModelForm):
    class Meta:
        model = Orderer
        fields = ('name', 'email', 'phone_number', 'password')
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name',
                'class': 'form-control',
                'placeholder': '이름',
                'data-validation-required-message': '이름을 입력해주세요.'}),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'class': 'form-control',
                'placeholder': 'Email',
                'data-validation-required-message': 'Email을 입력해주세요.'}),
            'phone_number': forms.NumberInput(attrs={
                'id': 'phone_number',
                'class': 'form-control',
                'placeholder': '연락처',
                'data-validation-required-message': '연락처를 입력해주세요.'}),
            'password': forms.PasswordInput(attrs={
                'id': 'password',
                'class': 'form-control',
                'placeholder': '비밀번호',
                'data-validation-required-message': '비밀번호를 입력해주세요.'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('eating_date', 'delivery_location')
        widgets = {
            'eating_date': DateTimeWidget(usel10n=True, bootstrap_version=3, attrs={
                'id': 'eating_date',
                'class': 'form-control',
                'placeholder': '고기 수령 날짜',
                'data-validation-required-message': '날짜를 선택해주세요.'}),
            'delivery_location': forms.TextInput(attrs={
                'id': 'delivery_location',
                'class': 'form-control',
                'placeholder': '배달 장소',
                'data-validation-required-message': '배달 장소를 입력해주세요.'}),
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = Orderer
        fields = ('name', 'email', 'password')
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name',
                'class': 'form-control',
                'placeholder': '이름',
                'data-validation-required-message': '이름을 입력해주세요.'}),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'class': 'form-control',
                'placeholder': 'Email',
                'data-validation-required-message': 'Email을 입력해주세요.'}),
            'password': forms.PasswordInput(attrs={
                'id': 'password',
                'class': 'form-control',
                'placeholder': '비밀번호',
                'data-validation-required-message': '비밀번호를 입력해주세요.'}),
        }
