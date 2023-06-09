from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Owner(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_cjqose'
    )
    about = models.TextField(blank=True)  

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s Pet Owner profile"


def create_owner(sender, instance, created, **kwargs):
    if created:
        Owner.objects.create(owner=instance)

post_save.connect(create_owner, sender=User)