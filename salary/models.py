from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Salary(models.Model):
    user = models.ForeignKey(User, null=True)
    bonus = models.DecimalField(max_digits=12, decimal_places=2)
    bonus_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_method = models.TextField()
