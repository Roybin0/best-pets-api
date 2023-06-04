from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet


class OwnerFollower(models.Model):
    """
    OwnerFollower model, related to 'owner' and 'followed'.
    'owner' is a User that is following a User.
    'followed_owner' is a User that is followed by 'owner'.
    """
    owner = models.ForeignKey(User, related_name='owner_following', on_delete=models.CASCADE)
    followed_owner = models.ForeignKey(User, related_name='followed_owner', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed_owner']

    def __str__(self):
        return f'{self.owner} is following user: {self.followed_owner}'


class PetFollower(models.Model):
    """
    PetFollower model, related to 'owner' and 'followed'.
    'owner' is a User that is following a User.
    'followed_pet' is a Pet that is followed by 'owner'.
    """
    owner = models.ForeignKey(User, related_name='pet_following', on_delete=models.CASCADE)
    followed_pet = models.ForeignKey(Pet, related_name='followed_pet', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed_pet']

    def __str__(self):
        return f'{self.owner} is following pet: {self.followed_pet}'