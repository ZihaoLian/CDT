from django.urls import path, re_path
from .views import ImageView
from django.views.static import serve
from django.conf import settings


urlpatterns = [
    path('api/v1/image/', ImageView.as_view({'post': 'create'})),
    re_path('media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    # re_path('detect/media(?P<path>.*)$', ImageView.as_view({'get', 'retrieve'}))
]