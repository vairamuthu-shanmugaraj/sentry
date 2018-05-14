from __future__ import absolute_import

from sentry.testutils import APITestCase
from sentry.integrations.bitbucket.installed import BitbucketInstalledEndpoint
from sentry.models import Integration


class BitbucketInstalledEndpointTest(APITestCase):
    def setUp(self):
        self.provider = 'bitbucket'
        self.path = '/extensions/bitbucket/installed/'

        self.name = 'Bitbucket'
        self.client_key = u'connection:123'
        self.public_key = u'123abcDEFg'
        self.shared_secret = u'G12332434SDfsjkdfgsd'
        self.base_url = u'https://bitbucket.org'
        self.domain_name = u'bitbucket.org'

        self.metadata = {
            'public_key': self.public_key,
            'shared_secret': self.shared_secret,
            'base_url': self.base_url,
            'domain_name': self.domain_name,
        }
        self.data_from_bitbucket = {
            u'key': u'sentry-bitbucket',
            u'eventType': u'installed',
            u'baseUrl': self.base_url,
            u'sharedSecret': self.shared_secret,
            u'publicKey': self.public_key,
            u'user': {
                u'username': u'sentryuser',
                u'display_name': u'Sentry User',
                u'account_id': u'123456t256371u',
                u'links': {
                    u'self': {u'herf': u'https://api.bitbucket.org/2.0/users/sentryuser/'},
                    u'html': {u'href': u'https://bitbucket.org/sentryuser/'},
                    u'avatar': {u'href': u'https://bitbucket.org/account/sentryuser/avatar/32/'},
                },
                u'created_on': u'2018-04-18T00:46:37.374621+00:00',
                u'is_staff': False,
                u'type': u'user',
                u'uuid': u'{e123-f456-g78910}'},
            u'productType': u'bitbucket',
            u'baseApiUrl': u'https://api.bitbucket.org',
            u'clientKey': self.client_key,
        }
        self.data_without_public_key = {
            'identity': {
                'bitbucket_client_id': self.client_key,
            }
        }

    def test_default_permissions(self):
        # Permissions must be empty so that it will be accessible to bitbucket.
        assert BitbucketInstalledEndpoint.authentication_classes == ()
        assert BitbucketInstalledEndpoint.permission_classes == ()

    def test_installed_with_public_key(self):
        response = self.client.post(
            self.path,
            data=self.data_from_bitbucket
        )
        assert response.status_code == 200
        integration = Integration.objects.get(
            provider=self.provider,
            external_id=self.client_key
        )
        assert integration.name == 'Bitbucket'
        assert integration.metadata == self.metadata

    def test_installed_without_public_key(self):
        integration = Integration.objects.get_or_create(
            provider=self.provider,
            external_id=self.client_key,
            defaults={
                'name': self.name,
                'metadata': self.metadata,
            }
        )[0]

        response = self.client.post(
            self.path,
            data=self.data_from_bitbucket
        )
        assert response.status_code == 200

        # assert no changes have been made to the integration
        integration_after = Integration.objects.get(
            provider=self.provider,
            external_id=self.client_key
        )
        assert integration.name == integration_after.name
        assert integration.metadata == integration_after.metadata