from django import forms
from django.contrib.auth import get_user_model
from decimal import Decimal


User = get_user_model()


class SendMoneyForm(forms.Form):
    """ Форма отправки денег списку ИНН """
    from_user = forms.ModelChoiceField(
        required=True,
        label='От кого',
        queryset=User.objects.filter(is_active=True),
    )
    to_users = forms.CharField(
        required=True,
        label='Кому',
        widget=forms.Textarea,
        help_text='Введите список ИНН через запятую.'
    )
    money = forms.DecimalField(
        required=True,
        label='Сумма перевода',
    )

    def clean_to_users(self):
        to_users = self.cleaned_data.get('to_users').replace(' ', '')
        from_user = self.cleaned_data.get('from_user')

        if not from_user:
            raise forms.ValidationError('Выберите откуда перечислять деньги.')

        inn_list = to_users.split(',')

        if len(inn_list) != len(set(inn_list)):
            raise forms.ValidationError('ИНН должны быть уникальными.')

        if not len(inn_list):
            raise forms.ValidationError('Список ИНН не может быть пустым.')

        users = User.objects.filter(inn__in=inn_list).exclude(pk=from_user.pk)
        if len(users) != len(inn_list):
            raise forms.ValidationError('Введите корректные ИНН.')

        return users

    def clean_money(self):
        money = Decimal(self.cleaned_data.get('money'))
        from_user = self.cleaned_data.get('from_user')

        if not from_user:
            raise forms.ValidationError('Выберите откуда перечислять деньги.')

        if money <= 0:
            raise forms.ValidationError('Сумма должна быть больше 0.')

        if from_user.money < money:
            raise forms.ValidationError('Не достаточно денег на счету.')

        return money
