from rest_framework.generics import ListAPIView

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from api.csvexport.renderers import ActivityCSVRenderer
from api.csvexport.serializers import ActivityCSVExportSerializer
from iati.models import Activity


class ActivityList(ListAPIView):
    """IATI representation for activities"""

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, ActivityCSVRenderer]
    queryset = Activity.objects.all()
    serializer_class = ActivityCSVExportSerializer
