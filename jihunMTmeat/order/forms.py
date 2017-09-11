from django import forms
from datetimewidget.widgets import DateTimeWidget

from order.models import Orderer


class OrdererForm(forms.ModelForm):
    class Meta:
        model = Orderer
        fields = ('name', 'email', 'phone_number', 'password', 'eating_date', 'is_delivery')
        widgets = {
            'eating_date': DateTimeWidget(usel10n=True, bootstrap_version=3),
        }

