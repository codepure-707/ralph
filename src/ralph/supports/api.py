# -*- coding: utf-8 -*-
import django_filters
from django.db.models import Prefetch
from rest_framework import serializers

from ralph.api import RalphAPISerializer, RalphAPIViewSet, router
from ralph.assets.api.serializers import (
    ServiceEnvironmentSimpleSerializer,
    StrField,
    TypeFromContentTypeSerializerMixin,
)
from ralph.assets.models import BaseObject
from ralph.lib.permissions.api import PermissionsForObjectFilter
from ralph.lib.visibility_scope.filters import visibility_scope_asset_support_filter
from ralph.supports.models import BaseObjectsSupport, Support, SupportType


class SupportTypeSerializer(RalphAPISerializer):
    class Meta:
        model = SupportType
        fields = "__all__"


class SupportTypeViewSet(RalphAPIViewSet):
    queryset = SupportType.objects.all()
    serializer_class = SupportTypeSerializer


class SupportSimpleSerializer(RalphAPISerializer):
    class Meta:
        model = Support
        fields = [
            "support_type",
            "contract_id",
            "name",
            "serial_no",
            "date_from",
            "date_to",
            "created",
            "remarks",
            "description",
            "url",
        ]
        _skip_tags_field = True


class SupportSerializer(TypeFromContentTypeSerializerMixin, RalphAPISerializer):
    __str__ = StrField(show_type=True)
    base_objects = serializers.HyperlinkedRelatedField(
        many=True, view_name="baseobject-detail", read_only=True
    )
    service_env = ServiceEnvironmentSimpleSerializer()

    class Meta:
        model = Support
        depth = 1
        exclude = ("content_type", "configuration_path")


class BaseObjectsFilter(django_filters.FilterSet):
    """
    select supports that are assigned to one of the assets
    e.g. /?base_objects=1,2,3

    """

    base_objects = django_filters.CharFilter(
        field_name="base_objects", method="filter_base_objects"
    )

    class Meta:
        model = Support
        fields = ("base_objects",)

    def filter_base_objects(self, queryset, name, value):
        if not value:
            return queryset
        try:
            ids = [int(x) for x in value.split(",")]
            return queryset.filter(base_objects__in=ids)
        except ValueError:
            return queryset.none()


class SupportViewSet(RalphAPIViewSet):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        PermissionsForObjectFilter,
    )
    filterset_class = BaseObjectsFilter
    select_related = [
        "region",
        "budget_info",
        "support_type",
        "property_of",
        "service_env",
        "service_env__service",
        "service_env__environment",
    ]
    prefetch_related = [
        "tags",
        Prefetch("base_objects", queryset=BaseObject.objects.all()),
    ]


class BaseObjectsSupportSerializer(RalphAPISerializer):
    support = SupportSimpleSerializer()
    baseobject = serializers.HyperlinkedRelatedField(
        view_name="baseobject-detail", read_only=True
    )

    class Meta:
        model = BaseObjectsSupport
        fields = "__all__"


class BaseObjectSupportViewSet(RalphAPIViewSet):
    queryset = BaseObjectsSupport.objects.all()
    serializer_class = BaseObjectsSupportSerializer
    select_related = ["baseobject", "support"]
    extended_filter_fields = {
        "base_object": ["baseobject"],
    }

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(visibility_scope_asset_support_filter(self.request.user))
        )


router.register(r"base-objects-supports", BaseObjectSupportViewSet)
router.register(r"supports", SupportViewSet)
router.register(r"support-types", SupportTypeViewSet)
urlpatterns = []
