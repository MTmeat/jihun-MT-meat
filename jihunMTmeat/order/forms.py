from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

from datetimewidget.widgets import DateTimeWidget

from order.models import Orderer, Order


class OrdererForm(forms.ModelForm):
    class Meta:
        model = Orderer
        fields = ('username', 'email', 'phone_number', 'password')
        widgets = {
            'username': forms.TextInput(attrs={
                'id': 'username',
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

    def is_valid(self, request):
        # run the parent validation first
        valid = super(OrdererForm, self).is_valid()

        if not valid:
            try:
                orderer = Orderer.objects.get(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    phone_number=request.POST['phone_number'],
                )

                user = authenticate(username=orderer.username, password=request.POST['password'])
                if user is not None:
                    return 'EXIST'

            except ObjectDoesNotExist:
                return False

        return valid


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
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={
                'id': 'username',
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
    def auth(self,request):
        try:

            orderer = Orderer.objects.get(
                username=request.POST.get('username'),
                email=request.POST.get('email'),
            )

            user = authenticate(username=orderer.username, password=request.POST.get('password'))
            if user is not None: # login success
                return user
            else: # login fail
                return None
        except ObjectDoesNotExist: # Not matching user Info
            return None
