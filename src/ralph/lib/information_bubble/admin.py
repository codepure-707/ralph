from django.contrib import admin

from ralph.admin.decorators import register
from ralph.admin.mixins import RalphAdmin
from ralph.lib.information_bubble.models import ServiceBasedInformationBubble



@register(ServiceBasedInformationBubble)
class ServiceBasedInformationBubbleAdmin(RalphAdmin):
    search_fields = ["name"]
