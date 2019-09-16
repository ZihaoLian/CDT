from django.urls import path, re_path
from .views import ImageView


urlpatterns = [
    path('api/v1/image/', ImageView.as_view({'post': 'create'})),
    re_path('media/(?P<path>.*)', ImageView.as_view({'get': 'retrieve'})),
    # path('image/', ImageView.as_view({'get': 'retrieve'})),
]