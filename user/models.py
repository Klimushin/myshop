from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.translation import gettext as _


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        verbose_name=_("user name"),
        related_name="profile",
    )

    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=100_000.00,
        validators=[MinValueValidator(0)],
        verbose_name=_("user's balance"),
    )

    class Meta:
        # db_table = "auth_userprofile"
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")