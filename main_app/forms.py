from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Payment, Event
from .choices import *


class MyForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class EventForm(forms.ModelForm):
    """
    Форма создания и обработки события
    """
    class Meta:
        model = Event
        fields = ('name', 'description', 'event_date')
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'event_date': 'Дата события'
        }


class PaymentForm(forms.ModelForm):
    """
    Форма создания и обработки платежей
    """
    class Meta:
        model = Payment
        percents_type = forms.ChoiceField(choices=PERCENT_CHOICES)
        fields = ('name', 'description', 'participants', 'creditor',
                  'percents_type', 'percents', 'period', 'total_loan_sum', 'destination', 'payment_date')
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'participants': 'Участники',
            'creditor': 'Кредитор',
            'percents_type': 'Тип процентов',
            'percents': 'Процент',
            'period': 'Период начисления процентов (в днях)',
            'total_loan_sum': 'Сумма долга',
            'destination': 'Перевести на (эл.кошелёк, номер телефона или карты)',
            'payment_date': 'Дата выдачи кредита'
        }
