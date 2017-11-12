from django.db import models

# Create your models here.


class Receipt(models.Model):
    creator = models.ForeignKey('accounts.Staff', on_delete=models.CASCADE)
    payer = models.CharField(max_length=30)
    payee = models.CharField(max_length=30)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    address = models.TextField()
    remarks = models.TextField(blank=True)
    items = models.ManyToManyField('Item')


class Item(models.Model):
    name = models.CharField(max_length=40)
    spec = models.CharField(max_length=10)
    number = models.PositiveIntegerField()
    unit = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_mount = models.DecimalField(max_digits=10, decimal_places=2)
