from rest_framework.viewsets import ModelViewSet
from .serializer import PersonSerializer
from .models import Person


class PersonView(ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
