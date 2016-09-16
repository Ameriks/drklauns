from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    ssn = models.CharField(_("Social Security Number"), blank=True, max_length=11)
    contract_no = models.CharField(_("Contract NR"), blank=True, max_length=50)
    contract_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    address = models.CharField(_("Address"), blank=True, max_length=255)
    bank_account = models.CharField(_("Bank Account"), blank=True, max_length=25)

    phone_number = models.CharField(_("Phone Number"), blank=True, max_length=25, default="+371")

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.full_name or self.username

    def save(self, *args, **kwargs):
        self.name = self.full_name
        self.is_staff = self.is_active
        super().save(*args, **kwargs)
