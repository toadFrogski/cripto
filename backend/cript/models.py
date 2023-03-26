from django.db import models
from django.utils.translation import gettext_lazy as _


class ADFGX(models.Model):

    class Methods(models.TextChoices):
        ADFGX = 'ADFGX', _('ADFGX')
        ADFGVX = 'ADFGVX', _('ADFGVX')

    class Types(models.TextChoices):
        ENCODE = 'EN', _('ENCODE')
        DECODE = 'DE', _('DECODE')

    original_message = models.TextField(null=False)
    key = models.CharField(max_length=15, null=False)
    encoded_message = models.TextField(null=True)
    method = models.CharField(
        max_length=10, choices=Methods.choices, default=Methods.ADFGX)
    type = models.CharField(
        max_length=2, choices=Types.choices
    )


class Playfair(models.Model):

    class Types(models.TextChoices):
        ENCODE = 'EN', _('ENCODE')
        DECODE = 'DE', _('DECODE')

    original_message = models.TextField(null=False)
    key = models.CharField(max_length=15, null=False)
    encoded_message = models.TextField(null=True)
    type = models.CharField(
        max_length=2, choices=Types.choices
    )

class Salsa(models.Model):

    class Types(models.TextChoices):
        ENCODE = 'EN', _('ENCODE')
        DECODE = 'DE', _('DECODE')

    original_message = models.TextField(null=False)
    key = models.CharField(max_length=15, null=False)
    encoded_message = models.TextField(null=True)
    type = models.CharField(
        max_length=2, choices=Types.choices
    )
