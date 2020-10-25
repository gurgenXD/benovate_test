from django.db.models import F


def send_money(from_user, to_users, money):
    """ Перевод денег от from_user к to_users, количество: money """
    money_for_user = money / len(to_users)

    from_user.money -= money
    from_user.save()

    to_users.update(money=F('money')+money_for_user)
