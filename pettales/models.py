from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from pets.models import Pet
from likes.models import Like


class PetTale(models.Model):
    """
    Pet tales model related to User and Pet. 
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_htulnf', blank=True
    )
    tldr = models.CharField(max_length=255, blank=False)
    tale = models.TextField(null=False)
    likes = GenericRelation(Like, related_query_name='pet_tales') 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pet.name}'s tale by {self.owner}"
