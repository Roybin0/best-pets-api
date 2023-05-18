from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet
from pettales.models import PetTale
from petpics.models import PetPic

class Comment(models.Model):
    """
    Comment model related to User. May also be associated with
    pets, pet tales or pet stories.  
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, blank=True, null=True)
    pet_tale = models.OneToOneField(PetTale, on_delete=models.CASCADE, blank=True, null=True)
    pet_pic = models.OneToOneField(PetPic, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s comment"  