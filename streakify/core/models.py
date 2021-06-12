from django.db import models
from six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from .behaviours import SlugMixin
from model_utils.models import TimeStampedModel
from django.conf import settings
from django.core.validators import RegexValidator
from streakify.core.validators import validator_ascii


class Country(SlugMixin):
    name = models.CharField(
        _("name"), max_length=100, blank=False, null=False, validators=[validator_ascii],
        help_text="The length of this field can't be longer than 100",
    ) 

    def __str__(self):
        return str(self.name)


@python_2_unicode_compatible
class Mobile(TimeStampedModel):
    mobile_regex = RegexValidator(regex=r"^[1-9]\d{9}$", message="Invalid Mobile Number")

    country_code_regex = RegexValidator(
        regex=r"^\+[0-9]{1,4}", message="Invalid Country Code"
    )
    country_code = models.CharField(
        _("Country Code"),
        validators=[country_code_regex],
        blank=False,
        null=False,
        max_length=5,
    )
    mobile = models.CharField(
        _("mobile number"),
        validators=[mobile_regex],
        blank=False,
        null=False,
        max_length=10,
        unique=True,
        help_text="Enter a valid 10 digit mobile number.",
    )
    verified = models.BooleanField(verbose_name=_("verified"), default=False)
    
    def __str__(self):
        return str(self.country_code + self.mobile)

    class Meta:
        unique_together = ('country_code', 'mobile',)

