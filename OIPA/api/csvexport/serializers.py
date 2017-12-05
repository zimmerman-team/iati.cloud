from rest_framework.serializers import CharField, SerializerMethodField

from api.activity.serializers import ActivitySerializer
from iati.models import Activity


class MySerializerMethodField(SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        if 'inner_source' in kwargs:
            self.inner_source = kwargs.pop('inner_source')
        super(MySerializerMethodField, self).__init__(method_name, **kwargs)

    def to_representation(self, value):
        from rest_framework.fields import get_attribute
        method = getattr(self.parent, self.method_name)
        value = method(value)
        val2 = get_attribute(value, self.inner_source.split('.'))
        return val2


class ActivityCSVExportSerializer(ActivitySerializer):
    activity_status_code = CharField(source='activity_status.code', default='')
    collaboration_type_code = CharField(source='collaboration_type.code', default='')
    default_aid_type_code = CharField(source='default_aid_type.code', default='')
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

    class Meta(ActivitySerializer.Meta):
        model = Activity
        fields = (
            'activity_status_code',
            'actual_end',
            'actual_start',
            'collaboration_type_code',
            'default_aid_type_code',
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
            'description'
        )
