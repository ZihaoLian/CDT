from django.urls import path
from .views import PersonView


urlpatterns = [
    path('people/', PersonView.as_view({'post': 'create'})),
    path('person/<str:pk>/',
         PersonView.as_view({'get': 'retrieve', 'put': 'partial_update'})),
]
