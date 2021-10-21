# Core Django Imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third-party app imports
from model_utils.models import TimeStampedModel

# Local Imports
from streakify.core.behaviours import StatusMixin
from streakify.core.validators import (
    validator_ascii,
    validator_country_code,
    validator_mobile_no,
)


class User(AbstractUser, StatusMixin, TimeStampedModel):
    """Default user for Streakify."""

    name = models.CharField(
        _("name"),
        max_length=100,
        blank=True,
        null=True,
        validators=[validator_ascii],
        help_text="The length of this field can't be longer than 100",
    )
    country_code = models.CharField(
        _("Country Code"),
        max_length=5,
        blank=True,
        null=True,
        validators=[validator_country_code],
        help_text="Enter a valid country code",
    )
    mobile_number = models.CharField(
        _("Mobile Number"),
        max_length=10,
        blank=True,
        null=True,
        validators=[validator_mobile_no],
        help_text="Enter a valid 10 digit mobile number.",
    )
    profile_pic = models.URLField(_("Profile Pic"), max_length=300, blank=True, null=True)
    device_id = models.CharField(_("Device ID"), max_length=300, blank=True, null=True)
    is_verified = models.BooleanField(_("is verified"), default=False)

    first_name = None
    last_name = None
