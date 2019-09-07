from rest_framework.viewsets import ModelViewSet
from .serializer import PersonSerializer
from .models import Person


# Create your views here.
class PersonView(ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
