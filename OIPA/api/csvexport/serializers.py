from rest_framework.serializers import CharField

from api.activity.serializers import ActivitySerializer
from iati.models import Activity


class ActivityCSVExportSerializer(ActivitySerializer):
    activity_status_code = CharField(source='activity_status.code', default='')
    collaboration_type_code = CharField(source='collaboration_type.code', default='')
    default_aid_type_code = CharField(source='default_aid_type.code', default='')
    default_finance_type_code = CharField(source='default_finance_type.code', default='')
    default_flow_type_code = CharField(source='default_flow_type.code', default='')
    default_tied_status_code = CharField(source='default_tied_status.code', default='')

    reporting_org = CharField(source='reporting_organisation.organisation.primary_name', default='')
    reporting_org_ref = CharField(source='reporting_organisation.ref', default='')
    reporting_org_type = CharField(source='reporting_organisation.organisation.type.name', default='')
    reporting_org_type_code = CharField(source='reporting_organisation.organisation.type.code', default='')

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
            'reporting_org_type_code'
        )
