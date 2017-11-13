from django.db import models
import uuid

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=80)
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('accounts.Staff', on_delete=models.CASCADE, null=True, related_name='owner_of_company')
    staff = models.ManyToManyField('accounts.Staff', related_name='staff_in_company')

    def __str__(self):
        return self.name
