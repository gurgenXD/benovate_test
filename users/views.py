from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from users.forms import SendMoneyForm
from users.services import send_money


User = get_user_model()


class SendMoneyView(View):
    def get(self, request):
        send_money_form = SendMoneyForm()

        context = {
            'send_money_form': send_money_form,
        }
        return render(request, 'users/send-money.html', context)

    def post(self, request):
        send_money_form = SendMoneyForm(request.POST)

        if send_money_form.is_valid():
            from_user = send_money_form.cleaned_data.get('from_user')
            money = send_money_form.cleaned_data.get('money')
            to_users = send_money_form.cleaned_data.get('to_users')

            send_money(from_user, to_users, money)

            return redirect('send_money')

        context = {
            'send_money_form': send_money_form,
        }
        return render(request, 'users/send-money.html', context)
