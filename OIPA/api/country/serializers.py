from django.urls import reverse
from rest_framework import serializers

import geodata
from api.fields import JSONField
from api.generics.serializers import DynamicFieldsModelSerializer
from api.region.serializers import RegionSerializer


class CountrySerializer(DynamicFieldsModelSerializer):

    code = serializers.CharField()
    name = serializers.CharField(required=False)
    url = serializers.HyperlinkedIdentityField(
        view_name='countries:country-detail', read_only=True)
    region = RegionSerializer(fields=('url', 'code', 'name'))
    un_region = RegionSerializer(fields=('url', 'code', 'name'))
    unesco_region = RegionSerializer(fields=('url', 'code', 'name'))
    location = JSONField(source='center_longlat.json')
    polygon = JSONField()
    activities = serializers.SerializerMethodField()
    budget_value = serializers.SerializerMethodField()

    def get_activities(self, obj):
        request = self.context.get('request')
        url = request.build_absolute_uri(reverse('activities:activity-list'))
        return url + '?recipient_country=' + obj.code

    def get_budget_value(self, obj):
        reporting_org_identifier = self.context.get(
            'request').query_params.get(
            'reporting_organisation_identifier', '')
        reporting_org_identifier_list = reporting_org_identifier.split(',')
        recipient_countries = obj.activityrecipientcountry_set.all()
        if reporting_org_identifier_list != ['']:
            requested_org_recipient_countries = recipient_countries.filter(
                activity__reporting_organisations__ref__in
                =reporting_org_identifier_list)
        else:
            requested_org_recipient_countries = recipient_countries
        total_budget = 0
        for country in requested_org_recipient_countries:
            try:
                total_budget = total_budget + country.budget_value
            except TypeError:
                pass
        return total_budget

    class Meta:
        model = geodata.models.Country
        fields = (
            'url',
            'code',
            'pk',
            'numerical_code_un',
            'name',
            'alt_name',
            'language',
            'region',
            'un_region',
            'unesco_region',
            'dac_country_code',
            'iso3',
            'alpha3',
            'fips10',
            'data_source',
            'activities',
            'location',
            'polygon',
            'budget_value'
        )
