from django.urls import path
from .views import PersonView


urlpatterns = [
    path('login/', PersonView.as_view({'get': 'list'})),
]
