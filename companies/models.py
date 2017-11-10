from django.db import models
import uuid

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=80)
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('accounts.Staff', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
