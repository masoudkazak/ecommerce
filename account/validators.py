from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^(\+98|0)?9\d{9}$'
    message = _(
        'Enter a valid username. '
        'Example: 09123456789'
    )
    flags = 0