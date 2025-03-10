from django.contrib.auth import get_user_model
from django.test import TestCase, TransactionTestCase
from factory import DjangoModelFactory

from ralph.accounts.tests.factories import UserFactory
from ralph.assets.tests.factories import ServiceFactory, ServiceEnvironmentFactory
from ralph.back_office.tests.factories import BackOfficeAssetFactory
from ralph.data_center.tests.factories import DataCenterAssetFactory
from ralph.lib.information_bubble.models import ServiceBasedInformationBubble


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


class TestServiceBasedInformationBubbleVisibility(TransactionTestCase):
    def setUp(self):
        super().setUp()
        self.information_bubble = ServiceBasedInformationBubbleFactory(name="foo")

        self.service_env_in_information_bubble = ServiceEnvironmentFactory()
        self.service_in_information_bubble = self.service_env_in_information_bubble.service
        self.information_bubble.services.set([self.service_in_information_bubble])

        self.service_env_outside_information_bubble = ServiceEnvironmentFactory()
        self.service_outside_information_bubble = self.service_env_outside_information_bubble.service

        self.user_outside_information_bubble = get_user_model().objects.create_superuser(username="user1", password="password", email="user1@email.pl", is_staff=True, is_active=True)
        self.user_in_information_bubble = get_user_model().objects.create_superuser(username="user2", password="password", email="user2@email.pl", is_staff=True, is_active=True)
        # get_user_model().objects.create(username="user3", password="password", email="user3@email.pl", is_staff=True, is_active=True)
        self.information_bubble.users.set([self.user_in_information_bubble])

        self.hw_in_information_bubble = DataCenterAssetFactory(service_env=self.service_env_in_information_bubble)
        self.hw_outside_information_bubble = DataCenterAssetFactory(
            service_env=self.service_env_outside_information_bubble
        )

        self.bo_in_information_bubble = BackOfficeAssetFactory(service_env=self.service_env_in_information_bubble)
        self.bo_outside_information_bubble = BackOfficeAssetFactory(
            service_env=self.service_env_outside_information_bubble
        )

    def test_user_in_information_bubble_can_see_1_hw(self):
        result = self.client.login(username="user2", password="password")
        # result = self.client.login(username="user3", password="password")
        import pdb; pdb.set_trace()
        self.assertEqual(result, True)
