from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Information(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    photo = models.ImageField(upload_to='photos/')
