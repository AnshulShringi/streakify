# Django imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from streakify.core.behaviours import StatusMixin, MobileMixin


class User(AbstractUser):
    """Default user for Streakify."""
    name = models.CharField(_("Name of User"), blank=True, max_length=255, default="")

    @property
    def user_profile(self):
        try:
            return UserProfile.objects.get(user=self)
        except UserProfile.DoesNotExist:
            return None



class UserProfile(StatusMixin, MobileMixin):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, blank=False, null=False, related_name="user_profile"
    )
    profile_pic = models.URLField(_("Profile Pic"), max_length=300, blank=True, null=True) 
    device_token = models.CharField(_("Device Message Token"), max_length=300, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)