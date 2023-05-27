from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import Like


pet_type_choices = [
    ("Cat", "Cat"),
    ("Dog", "Dog"),
    ("Hamster", "Hamster"),
    ("Horse", "Horse"),
    ("Reptile", "Reptile"),
    ("Rabbit", "Rabbit"),
    ("Other", "Other"),
]


class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    pet_type = models.CharField(max_length=50, choices=pet_type_choices, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_cjqose'
    )
    about = models.TextField(blank=True)
    likes = GenericRelation(Like, related_query_name='pets') 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s {self.pet_type} {self.name}"
