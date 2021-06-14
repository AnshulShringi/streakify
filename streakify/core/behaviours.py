from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import StatusMixinManager
from .utils import create_slug
from .validators import validator_ascii
from django.core.validators import RegexValidator


class StatusMixin(models.Model):
    is_active = models.BooleanField(_("active"), default=True, blank=False, null=False)
    is_deleted = models.BooleanField(
        _("deleted"), default=False, blank=False, null=False
    )

    objects = StatusMixinManager()

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()

    def remove(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()

    def has_changed(self, field):
        model = self.__class__.__name__
        return getattr(self, field) != getattr(
            self, "_" + model + "__original_" + field
        )

    def save(self, *args, **kwargs):
        """
        Makes sure that the ``is_active`` is ``False`` when ``is_deleted`` is ``True``.
        """
        if self.is_deleted:
            self.is_active = False
        super(StatusMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=255)

    def save(self, *args, **kwargs):
        """
        slug  shouldn't have spaces
        """
        if not self.slug:
            self.slug = create_slug(self)
        if self.slug:
            self.slug = self.slug.replace(" ", "")
        super(SlugMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


upload_location="/images"


class ImageMixin(models.Model):
    image = models.ImageField(
        _("image"), upload_to=upload_location, null=True, blank=True
    )
    image_alt = models.CharField(
        _("image alt"), max_length=100, blank=True, validators=[validator_ascii]
    )

    class Meta:
        abstract = True


class MobileMixin(models.Model):
    regex = RegexValidator(regex=r"^[1-9]\d{9}$", message="Invalid Mobile Number")
    mobile_number = models.CharField(
        _("mobile number"),
        validators=[regex],
        blank=False,
        null=False,
        max_length=10,
        help_text="Enter a valid 10 digit mobile number.",
    )
    country = models.ForeignKey("core.Country", on_delete=models.CASCADE, blank=False, null=False)
    verified = models.BooleanField(verbose_name=_("verified"), default=False)

    class Meta:
        abstract = True
        unique_together = ('country_code', 'mobile')

    @property
    def get_phone(self):
        return "%s%s" % (self.country.country_code, self.mobile)