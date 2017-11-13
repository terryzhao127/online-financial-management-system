from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=30, null=True)
    age = models.PositiveSmallIntegerField(null=True)
    workplaces = models.ManyToManyField('companies.Company', related_name='workplace_of_staff')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_staff(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user=instance)
    instance.staff.save()
