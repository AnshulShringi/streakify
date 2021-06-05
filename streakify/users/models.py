# Django imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

# Local imports
from .managers import CustomUserManager


class User(AbstractUser):
    """Default user for Streakify."""
    username_validator = UnicodeUsernameValidator()

    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    country_code = models.CharField(_("Country Code"), max_length=4)
    mobile_number = models.CharField(_("Mobile Number"), max_length=10)
    phone = models.CharField(_("Phone"), unique=True, max_length=14)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = None
    last_name = None 

    USERNAME_FIELD = 'phone'
    objects = CustomUserManager()

    class Meta:
        unique_together = ('country_code', 'mobile_number',)
    
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        if self.country_code and self.mobile_number:
            self.phone = self.country_code + self.mobile_number
        super(User, self).save(*args, **kwargs)
