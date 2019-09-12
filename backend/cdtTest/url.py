from django.urls import path
from .views import CdtTestView


urlpatterns = [
    path('test/', CdtTestView.as_view({'post': 'create'})),
]
