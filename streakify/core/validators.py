# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.validators import RegexValidator

validator_ascii = RegexValidator(regex=r"^[\x00-\x7F]*$", message="Only ASCII characters allowed")
validator_mobile_no = RegexValidator(regex=r"^[1-9]\d{9}$", message="Invalid Mobile Number")
validator_country_code = RegexValidator(regex=r"^\+[0-9]{1,4}", message="Invalid Country Code")
