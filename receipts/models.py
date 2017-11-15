from django.db import models

# Create your models here.


class Receipt(models.Model):
    creator = models.ForeignKey('accounts.Staff', on_delete=models.CASCADE)
    payer = models.CharField(max_length=30)
    payee = models.CharField(max_length=30)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    address = models.CharField(max_length=80)
    notes = models.CharField(max_length=80, blank=True)
    items = models.ManyToManyField('Item')

    def __str__(self):
        return str(self.id)


class Item(models.Model):
    name = models.CharField(max_length=40)
    spec = models.CharField(max_length=10)
    number = models.PositiveIntegerField()
    unit = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
