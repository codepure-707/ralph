from django.db import models
from django.utils.translation import ugettext_lazy as _

from ralph.lib.mixins.models import AdminAbsoluteUrlMixin, NamedMixin


class ServiceBasedInformationBubble(AdminAbsoluteUrlMixin, NamedMixin):
    services = models.ManyToManyField(
        "assets.Service",
        related_name="information_bubbles",
        blank=True
    )
    class Meta:
        verbose_name = _("Service-based Information Bubble")
