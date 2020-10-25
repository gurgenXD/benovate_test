from django.urls import path
from users.views import SendMoneyView


urlpatterns = [
    path('send-money', SendMoneyView.as_view(), name='send_money'),
]
