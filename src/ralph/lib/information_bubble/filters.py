from django.db.models import Q

from ralph.assets.models import Service
from ralph.lib.information_bubble.models import ServiceBasedInformationBubble


def information_bubbles_for_user(user):
    return ServiceBasedInformationBubble.objects.filter(
        Q(id__in=user.service_information_bubbles.all())
        | Q(group__in=user.groups.all())
    )


def information_bubble_filter(user):
    if user.is_superuser:
        return Q()

    bubbles = information_bubbles_for_user(user)
    if not bubbles:
        return Q()

    return Q(service_env__service__in=Service.objects.filter(information_bubbles__in=bubbles))


def information_bubble_asset_support_filter(user):
    """Only show BaseObjectsSupport for which assets belong to the service"""
    if user.is_superuser:
        return Q()

    bubbles = information_bubbles_for_user(user)
    if not bubbles:
        return Q()

    return Q(
        baseobject__service_env__service__in=Service.objects.filter(information_bubbles__in=bubbles)
    )
