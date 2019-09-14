from rest_framework.viewsets import ModelViewSet
from .serializer import FileSerializer
from .models import File
from person.models import Person


# Create your views here.
class FileView(ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        file = request.data.get('file')
        testTime = request.data.get('testTime')
        person = request.data.get('person')

        