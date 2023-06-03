from django.db import models
from django.contrib.auth.models import User
from pets.models import Pet


class Follower(models.Model):
    """
    Follower model, related to 'owner' and 'followed'.
    'owner' is a User that is following a User.
    'followedOwner' is a User that is followed by 'owner'.
    'followedPet' is a Pet that is followed by 'owner'.
    """
    owner = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )
    followed_owner = models.ForeignKey(
        User, related_name='followedOwner', on_delete=models.CASCADE, blank=True, null=True
    )
    followed_pet = models.ForeignKey(
        Pet, related_name='followedPet', on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed_owner', 'followed_pet']

    def __str__(self):
        if self.followed_owner:
            return f'{self.owner} is following user: {self.followed_owner}'
        elif self.followed_pet:
            return f'{self.owner} is following pet: {self.followed_pet}'
        else:
            return f'{self.owner} is not following anyone'