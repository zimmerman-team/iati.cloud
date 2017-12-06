from rest_framework.fields import get_attribute
from rest_framework.serializers import CharField, SerializerMethodField

from api.activity.serializers import ActivitySerializer
from iati.models import Activity


class MySerializerMethodField(SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        if 'inner_source' in kwargs:
            self.inner_source = kwargs.pop('inner_source')
        super(MySerializerMethodField, self).__init__(method_name, **kwargs)

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        value = method(value)
        val2 = get_attribute(value, self.inner_source.split('.'))
        return val2


class ActivityCSVExportSerializer(ActivitySerializer):
    activity_status_code = CharField(source='activity_status.code', default='')
    currency = SerializerMethodField(default='')
    collaboration_type_code = CharField(source='collaboration_type.code', default='')
    default_aid_type_code = CharField(source='default_aid_type.code', default='')
    default_currency = CharField(source='default_currency.code', default='')
    default_finance_type_code = CharField(source='default_finance_type.code', default='')
    default_flow_type_code = CharField(source='default_flow_type.code', default='')
    default_tied_status_code = CharField(source='default_tied_status.code', default='')

    reporting_org = MySerializerMethodField(
        method_name='get_reporting_organization',
        inner_source='organisation.primary_name',
        default='')
    reporting_org_ref = MySerializerMethodField(
        method_name='get_reporting_organization',
        inner_source='ref',
        default='')
    reporting_org_type = MySerializerMethodField(
        method_name='get_reporting_organization',
        inner_source='organisation.type.name',
        default='')
    reporting_org_type_code = MySerializerMethodField(
        method_name='get_reporting_organization',
        inner_source='organisation.type.code',
        default='')
    title = SerializerMethodField(default='')
    description = SerializerMethodField(default='')

    recipient_country_code = SerializerMethodField(default='')
    recipient_country_description = SerializerMethodField(default='')
    recipient_country_percentage = SerializerMethodField(default='')

    recipient_region_code = SerializerMethodField(default='')
    recipient_region_description = SerializerMethodField(default='')
    recipient_region_percentage = SerializerMethodField(default='')

    sector_code = SerializerMethodField(default='')
    sector_description = SerializerMethodField(default='')
    sector_percentage = SerializerMethodField(default='')
    sector_vocabulary = SerializerMethodField(default='')
    sector_vocabulary_code = SerializerMethodField(default='')

    def get_currency(self, obj):
        qs = obj.transaction_set.distinct('currency')
        if qs.count() == 1:
            transaction = obj.transaction_set.first()
            if transaction is not None:
                return transaction.currency.code
        elif qs.count() > 1:
            return u'Mixed currency!'

    def get_reporting_organization(self, obj):
        return obj.reporting_organisations.first()

    def get_title(self, obj):
        narrative = obj.title.narratives.filter(language=obj.default_lang).first()
        if narrative is not None:
            return narrative.content

    def get_description(self, obj):
        description = obj.description_set.filter(
            narratives__language=obj.default_lang).first()
        if description is not None:
            narrative = description.narratives.filter(language=obj.default_lang).first()
            if narrative is not None:
                return narrative.content

    def get_queryset_property_as_csv(self, queryset, attribute):
        """Return a list of 'attribute' values as CSV based on a queryset"""
        values = []
        for rc in queryset:
            val = get_attribute(rc, attribute.split('.'))
            if val is not None:
                values.append(unicode(val))
            else:
                values.append('')
        return ';'.join(values)

    # recipient countries

    def get_recipient_country_code(self, obj):
        return self.get_queryset_property_as_csv(obj.get_recipient_countries(),
                                                 'country.code')

    def get_recipient_country_description(self, obj):
        return self.get_queryset_property_as_csv(obj.get_recipient_countries(),
                                                 'country.name')

    def get_recipient_country_percentage(self, obj):
        return self.get_queryset_property_as_csv(obj.get_recipient_countries(),
                                                 'percentage')

    def get_recipient_region_code(self, obj):
        return self.get_queryset_property_as_csv(obj.get_recipient_regions(),
                                                 'region.code')

    def get_recipient_region_description(self, obj):
        return self.get_queryset_property_as_csv(obj.get_recipient_regions(),
                                                 'region.name')

    def get_recipient_region_percentage(self, obj):
        return self.get_queryset_property_as_csv(obj.get_recipient_regions(),
                                                 'percentage')

    # sectors

    def get_sector_code(self, obj):
        return self.get_queryset_property_as_csv(obj.get_sectors(), 'sector.code')

    def get_sector_description(self, obj):
        return self.get_queryset_property_as_csv(obj.get_sectors(), 'sector.description')

    def get_sector_percentage(self, obj):
        return self.get_queryset_property_as_csv(obj.get_sectors(), 'percentage')

    def get_sector_vocabulary(self, obj):
        return self.get_queryset_property_as_csv(obj.get_sectors(), 'sector.vocabulary.name')

    def get_sector_vocabulary_code(self, obj):
        return self.get_queryset_property_as_csv(obj.get_sectors(), 'sector.vocabulary.code')

    class Meta(ActivitySerializer.Meta):
        model = Activity
        fields = (
            'activity_status_code',
            'actual_end',
            'actual_start',
            'collaboration_type_code',
            'currency',
            'default_aid_type_code',
            'default_currency',
            'default_finance_type_code',
            'default_flow_type_code',
            'default_lang',
            'default_tied_status_code',
            'hierarchy',
            'iati_identifier',
            'last_updated_datetime',
            'planned_end',
            'planned_start',
            'reporting_org',
            'reporting_org_ref',
            'reporting_org_type',
            'reporting_org_type_code',
            'title',
            'description',
            'recipient_country_code',
            'recipient_country_description',
            'recipient_country_percentage',
            'recipient_region_code',
            'recipient_region_description',
            'recipient_region_percentage',

            'sector_code',
            'sector_description',
            'sector_percentage',
            'sector_vocabulary',
            'sector_vocabulary_code'
        )
