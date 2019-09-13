from rest_framework.viewsets import ModelViewSet
from .serializer import FileSerializer
from .models import File


# Create your views here.
class FileView(ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()
