from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Salary(models.Model):
    payer = models.ForeignKey('accounts.Staff', on_delete=models.CASCADE, related_name="staff_who_pay_others")
    payee = models.ForeignKey('accounts.Staff', on_delete=models.CASCADE, related_name="staff_who_get_salary")
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.payee.full_name