from django.urls import path
from .views import CdtTestView


urlpatterns = [
    path('', CdtTestView.as_view({'post': 'create'})),
]
