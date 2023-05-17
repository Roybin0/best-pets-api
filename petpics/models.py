from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet


class PetPic(models.Model):
    """
    Pet picture model related to User and Pet. 
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(Pet, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_htulnf', null=False
    )
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}'s pic by {self.owner}"