from django.contrib import admin
from django.urls import include, path

from publish.api import DandisetViewSet, NWBFileViewSet, SubjectViewSet

from rest_framework import routers


router = routers.DefaultRouter()
router.register('dandiset', DandisetViewSet)
router.register('subject', SubjectViewSet)
router.register('nwb', NWBFileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
