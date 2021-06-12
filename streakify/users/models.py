# Django imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Streakify."""

    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)

    def __str__(self):
        return self.username

    @property
    def user_profile(self):
        try:
            return UserProfile.objects.get(user=self)
        except UserProfile.DoesNotExist:
            return None



class UserProfile(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, blank=False, null=False, related_name="user_info"
    )
    mobile = models.OneToOneField("core.Mobile", on_delete=models.CASCADE, blank=False, null=False)
    user_image = models.ImageField(_("Profile Image"), upload_to="", null=True, blank=True)

    def __str__(self):
        return str(self.user.username)