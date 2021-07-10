from django.db import models
from django.utils.translation import ugettext_lazy as _
from streakify.core.behaviours import SlugMixin, StatusMixin
from model_utils.models import TimeStampedModel
from django.core.validators import RegexValidator
from streakify.core.validators import validator_ascii


class Country(SlugMixin):
    country_code_regex = RegexValidator(
        regex=r"^\+[0-9]{1,4}", message="Invalid Country Code"
    )
    
    name = models.CharField(
        _("name"), max_length=100, blank=True, null=True, validators=[validator_ascii],
        help_text="The length of this field can't be longer than 100",
    ) 
    country_code = models.CharField(
        _("Country Code"),
        validators=[country_code_regex],
        blank=False,
        null=False,
        unique=True,
        max_length=5
    )

    def __str__(self):
        return str(self.country_code)


class ImageModel(StatusMixin, TimeStampedModel):
    image = models.ImageField(_("Image"), upload_to="images")
    
    def __str__(self):
        return str(self.id)