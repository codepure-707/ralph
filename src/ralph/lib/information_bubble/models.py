from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ralph.lib.mixins.models import AdminAbsoluteUrlMixin, NamedMixin


class ServiceBasedInformationBubble(AdminAbsoluteUrlMixin, NamedMixin):
    services = models.ManyToManyField(
        "assets.Service",
        related_name="information_bubbles",
        blank=True
    )
    group = models.ForeignKey(
        Group,
        related_name="information_bubbles",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _("Service-based Information Bubble")
