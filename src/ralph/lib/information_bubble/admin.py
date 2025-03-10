from django.contrib import admin

from ralph.admin.decorators import register
from ralph.admin.mixins import RalphAdmin
from ralph.lib.information_bubble.models import ServiceBasedInformationBubble



@register(ServiceBasedInformationBubble)
class ServiceBasedInformationBubbleAdmin(RalphAdmin):
    pass
    # show_custom_fields_values_summary = False
    # search_fields = ["service__name", "environment__name"]
    # list_select_related = ["service", "environment"]
    # raw_id_fields = ["service", "environment"]
    # resource_class = resources.ServiceEnvironmentResource
    # fields = ("service", "environment", "remarks", "tags")
