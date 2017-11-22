from django.core.urlresolvers import reverse
from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from iati.factory import iati_factory
from iati.factory.iati_factory import ActivityFactory, ReportingOrganisationFactory
from iati.permissions.factories import OrganisationUserFactory
from iati_codelists.factory.codelist_factory import OrganisationTypeFactory


class TestActivityEndpoints(APITestCase):
    rf = RequestFactory()
    c = APIClient(HTTP_ACCEPT='application/json')

    def setUp(self):
        user = OrganisationUserFactory.create(user__username='test1')
        self.c.force_authenticate(user.user)

    def test_activities_endpoint(self):
        url = reverse('activities:activity-list')
        expect_url = '/api/activities/'
        msg = 'activities endpoint should be located at {0}'
        assert url == expect_url, msg.format(expect_url)
        response = self.c.get(url)
        self.assertTrue(status.is_success(response.status_code))

    def test_filter_activities_by_reporting_organisation_type(self):
        # create data to filter for
        org1 = ReportingOrganisationFactory.create(
            activity=ActivityFactory.create(iati_identifier='IATI-000001'),
            type=OrganisationTypeFactory.create(code='22'))
        # create additional data to test result count
        ReportingOrganisationFactory.create(
            activity=ActivityFactory.create(iati_identifier='IATI-000002'),
            type=OrganisationTypeFactory.create(code='10'))

        response = self.c.get(reverse('activities:activity-list'), {
            'reporting_organisation_type': org1.type.code
        })
        self.assertTrue(status.is_success(response.status_code))
        results = response.json()['results']
        assert len(results) == 1
        assert org1.activity.iati_identifier in results[0]['iati_identifier']

    def test_activity_detail_endpoint(self):
        iati_factory.ActivityFactory.create(iati_identifier='activity_id')
        url = reverse('activities:activity-detail', args={'activity_id'})
        msg = 'activity detail endpoint should be located at {0}'
        expect_url = '/api/activities/activity_id/'
        assert url == expect_url, msg.format(expect_url)
        response = self.c.get(url)
        self.assertTrue(status.is_success(response.status_code))

    def test_activity_aggregations_endpoint(self):
        url = reverse('activities:activity-aggregations')
        msg = 'activity aggregations endpoint should be located at {0}'
        expect_url = '/api/activities/aggregations/'
        assert url == expect_url, msg.format(expect_url)
        response = self.c.get(expect_url,
                              {'group_by': 'recipient_country', 'aggregations': 'count'},
                              format='json')
        self.assertTrue(status.is_success(response.status_code))

    def test_transactions_endpoint(self):
        url = reverse('activities:activity-transactions', args={'activity_id'})
        msg = 'activity transactions endpoint should be located at {0}'
        expect_url = '/api/activities/activity_id/transactions/'
        assert url == expect_url, msg.format(expect_url)
        response = self.c.get(url)
        self.assertTrue(status.is_success(response.status_code))
