# Django imports
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone number is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, country_code, mobile_number, **extra_fields):
        """
        Create and save a User with the given phone number.
        """
        if not country_code and not mobile_number:
            raise ValueError(_('Country code and Mobile number required'))
        user = self.model(country_code=country_code, mobile_number=mobile_number, **extra_fields)
        user.save()
        return user

    def create_superuser(self, country_code, mobile_number, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(country_code, mobile_number, **extra_fields)