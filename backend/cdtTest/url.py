from django.urls import path, re_path
from .views import CdtTestView


urlpatterns = [
    re_path('(?P<openId>.*)$', CdtTestView.as_view({'get': 'list'})),
]
