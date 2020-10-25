from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal


class User(AbstractUser):
    """ Расширение стандартной модели Django """
    inn = models.CharField('ИНН', max_length=12, unique=True, null=True,
        blank=True, validators=[RegexValidator('^[\d]+$')])

    money = models.DecimalField('Счёт', max_digits=11, decimal_places=2,
        default=0.00, validators=[MinValueValidator(Decimal('0.00'))])
