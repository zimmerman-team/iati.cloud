from django.conf.urls import url

from api.csvexport.views import ActivityList

urlpatterns = [
    url(r'^activities', ActivityList.as_view(), name='activity-list'),
]
