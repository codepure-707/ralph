from ralph.admin.decorators import register
from ralph.admin.mixins import RalphAdmin
from ralph.lib.visibility_scope.models import ServiceBasedVisibilityScope


@register(ServiceBasedVisibilityScope)
class ServiceBasedVisibilityScopeAdmin(RalphAdmin):
    search_fields = ["name"]
