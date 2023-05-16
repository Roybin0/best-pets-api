from django.db import models
from django.contrib.auth.models import User


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

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s pet {self.pet_type}"
