from rest_framework.viewsets import ModelViewSet
from .serializer import CdtTestSerializer
from .models import CdtTest


# Create your views here.
class CdtTestView(ModelViewSet):
    serializer_class = CdtTestSerializer
    queryset = CdtTest.objects.all()

