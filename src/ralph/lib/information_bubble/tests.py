from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse
from factory import DjangoModelFactory
from rest_framework.test import APITestCase

from ralph.accounts.tests.factories import UserFactory
from ralph.assets.tests.factories import (
    ServiceEnvironmentFactory,
    ServiceFactory
)
from ralph.data_center.models import DataCenterAsset
from ralph.data_center.tests.factories import DataCenterAssetFactory
from ralph.lib.information_bubble.models import ServiceBasedInformationBubble
from ralph.supports.models import BaseObjectsSupport, Support
from ralph.virtual.models import VirtualServer


class ServiceBasedInformationBubbleFactory(DjangoModelFactory):
    class Meta:
        model = ServiceBasedInformationBubble
        django_get_or_create = ["name"]


class TestServiceBasedInformationBubbleCreation(TestCase):
    def test_create_information_bubble(self):
        ib = ServiceBasedInformationBubbleFactory(name="foo")
        ib.services.set([ServiceFactory(), ServiceFactory()])
        self.assertEqual(len(ib.services.all()), 2)

    def test_assign_user_to_information_bubble(self):
        ib = ServiceBasedInformationBubbleFactory(name="foo")
        ib.services.set([ServiceFactory(), ServiceFactory()])
        user = UserFactory()
        ib.users.set([user])
        self.assertEqual(user.service_information_bubbles.first().pk, ib.pk)


class TestServiceBasedInformationBubbleVisibility(APITestCase):
    def setUp(self):
        super().setUp()
        self.information_bubble = ServiceBasedInformationBubbleFactory(name="foo")

        self.service_env_in_information_bubble = ServiceEnvironmentFactory()
        self.service_in_information_bubble = self.service_env_in_information_bubble.service
        self.information_bubble.services.set([self.service_in_information_bubble])

        self.service_env_outside_information_bubble = ServiceEnvironmentFactory()
        self.service_outside_information_bubble = (
            self.service_env_outside_information_bubble.service
        )

        self.user_outside_information_bubble = get_user_model().objects.create(
            username="user1",
            is_staff=True,
            is_active=True
        )
        self.user_in_information_bubble = get_user_model().objects.create(
            username="user2",
            is_staff=True,
            is_active=True
        )

        content_types = [ContentType.objects.get_for_model(m) for m in (
            DataCenterAsset,
            VirtualServer,
            Support,
            BaseObjectsSupport
        )]
        permissions = Permission.objects.filter(content_type__in=content_types)
        for user in (self.user_in_information_bubble, self.user_outside_information_bubble):
            user.user_permissions.add(*permissions)

        self.information_bubble.users.set([self.user_in_information_bubble])


class TestDataCenterAssetVisibilityInInformationBubble(
    TestServiceBasedInformationBubbleVisibility
):
    def setUp(self):
        super().setUp()
        self.hw_in_information_bubble = DataCenterAssetFactory(
            service_env=self.service_env_in_information_bubble
        )
        self.hw_outside_information_bubble = DataCenterAssetFactory(
            service_env=self.service_env_outside_information_bubble
        )
        self.hw_without_service_env = DataCenterAssetFactory(
            service_env=None
        )

        permissions = Permission.objects.filter(
            content_type__in=ContentType.objects.get_for_model(DataCenterAsset)
        )
        for user in (self.user_in_information_bubble, self.user_outside_information_bubble):
            user.user_permissions.add(*permissions)

    def test_user_in_information_bubble_can_see_1_hw(self):
        self.client.force_authenticate(self.user_in_information_bubble)
        url = reverse("datacenterasset-list")
        response = self.client.get(url)
        self.assertEqual(response.json()['count'], 1)

    def test_user_outside_information_bubble_can_see_3_hws(self):
        self.client.force_authenticate(self.user_outside_information_bubble)
        url = reverse("datacenterasset-list")
        response = self.client.get(url)
        self.assertEqual(response.json()['count'], 3)
