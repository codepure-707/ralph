from ralph.api import RalphAPISerializer, RalphAPIViewSet, router
from ralph.lib.information_bubble.models import ServiceBasedInformationBubble


class ServiceBasedInformationBubbleSerializer(RalphAPISerializer):
    class Meta:
        model = ServiceBasedInformationBubble
        fields = "__all__"


class ServiceBasedInformationBubbleViewSet(RalphAPIViewSet):
    queryset = ServiceBasedInformationBubble.objects.all()
    serializer_class = ServiceBasedInformationBubbleSerializer


router.register(r"service-based-information-bubbles", ServiceBasedInformationBubbleViewSet)
urlpatterns = []
