from ralph.api import RalphAPISerializer, RalphAPIViewSet, router
from ralph.lib.visibility_scope.models import ServiceBasedVisibilityScope


class ServiceBasedVisibilityScopeSerializer(RalphAPISerializer):
    class Meta:
        model = ServiceBasedVisibilityScope
        fields = "__all__"


class ServiceBasedVisibilityScopeViewSet(RalphAPIViewSet):
    queryset = ServiceBasedVisibilityScope.objects.all()
    serializer_class = ServiceBasedVisibilityScopeSerializer


router.register(r"service-based-visibility-scopes", ServiceBasedVisibilityScopeViewSet)
urlpatterns = []
