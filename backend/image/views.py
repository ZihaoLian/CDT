from rest_framework.viewsets import ModelViewSet
from .serializer import ImageSerializer
from .models import Image


# Create your views here.
class ImageView(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

