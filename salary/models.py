from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Salary(models.Model):
    uploader = models.ForeignKey('accounts.Staff', on_delete=models.CASCADE, related_name="staff_who_upload_salary")
    staff = models.ForeignKey('accounts.Staff', on_delete=models.CASCADE, related_name="staff_who_get_salary")
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
