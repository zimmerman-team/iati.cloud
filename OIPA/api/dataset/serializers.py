from django.urls import reverse
from rest_framework.serializers import (
    HyperlinkedIdentityField, HyperlinkedRelatedField, ModelSerializer,
    SerializerMethodField
)

from api.generics.serializers import DynamicFieldsModelSerializer
from iati.models import Activity
from iati_synchroniser.models import Dataset, DatasetNote, Publisher


class DatasetNoteSerializer(ModelSerializer):
    class Meta:
        model = DatasetNote
        fields = (
            'model',
            'iati_identifier',
            'exception_type',
            'model',
            'field',
            'message',
            'line_number',
            'variable')


class SimplePublisherSerializer(DynamicFieldsModelSerializer):

    url = HyperlinkedIdentityField(view_name='publishers:publisher-detail')

    class Meta:
        model = Publisher
        fields = (
            'id',
            'url',
            'publisher_iati_id',
            'display_name',
            'name')


class SimpleDatasetSerializer(DynamicFieldsModelSerializer):
    url = HyperlinkedIdentityField(view_name='datasets:dataset-detail')
    publisher = HyperlinkedRelatedField(
        view_name='publishers:publisher-detail',
        read_only=True)
    type = SerializerMethodField()

    class Meta:
        model = Dataset
        fields = (
            'id',
            'iati_id',
            'type',
            'url',
            'name',
            'title',
            'filetype',
            'publisher',
            'source_url',
            'iati_version',
            'added_manually',
        )

    def get_type(self, obj):
        return obj.get_filetype_display()


class DatasetSerializer(DynamicFieldsModelSerializer):

    url = HyperlinkedIdentityField(view_name='datasets:dataset-detail')
    publisher = SimplePublisherSerializer()
    filetype = SerializerMethodField()
    activities = SerializerMethodField()
    activity_count = SerializerMethodField()
    notes = HyperlinkedIdentityField(
        view_name='datasets:dataset-notes',)

    DatasetNoteSerializer(many=True, source="datasetnote_set")

    class Meta:
        model = Dataset
        fields = (
            'id',
            'iati_id',
            'url',
            'name',
            'title',
            'filetype',
            'publisher',
            'source_url',
            'activities',
            'activity_count',
            'date_created',
            'date_updated',
            'last_found_in_registry',
            'iati_version',
            'sha1',
            'note_count',
            'notes',
            'added_manually',
            'is_parsed',
            'export_in_progress',
            'parse_in_progress',
        )

    def get_filetype(self, obj):
        return obj.get_filetype_display()

    def get_activities(self, obj):
        request = self.context.get('request')
        url = request.build_absolute_uri(reverse('activities:activity-list'))
        return url + '?dataset=' + str(obj.id)

    def get_activity_count(self, obj):
        return Activity.objects.filter(dataset=obj.id).count()
