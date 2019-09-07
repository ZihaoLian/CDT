from rest_framework.serializers import ModelSerializer
from .models import CdtTest


class CdtTestSerializer(ModelSerializer):
    class Meta:
        model = CdtTest
        fields = '__all__'

