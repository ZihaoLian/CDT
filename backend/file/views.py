from rest_framework.viewsets import ModelViewSet
from .serializer import FileSerializer
from django.core.files.base import ContentFile
from .models import File
from cdtTest.models import CdtTest
from person.models import Person
from rest_framework.response import Response
from rest_framework import status
from public import code, msg, config
import time


# Create your views here.
class FileView(ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()

    def create(self, request, *args, **kwargs):
        ret = {
            code.FIELD_NAME: code.TEST_SUCCESS,
            msg.FIELD_NAME: None
        }

        file_name = request.data.get('fileName')
        file = request.FILES['file']
        test_time = request.data.get('testTime')
        person = request.data.get('person')
        hand_time = request.data.get('handTime')
        file_url = config.BASE_URL + 'file/' + file.name

        try:
            if file_name is not None and file is not None and test_time is not None and person is not None:
                cdt_obj = CdtTest(test_time=test_time, hand_time=hand_time, person_id=person)
                cdt_obj.save()

                file_obj = File(file=file)
                file_obj.file_name = file_name
                file_obj.test_id = cdt_obj.id
                file_obj.file_url = file_url
                file_obj.save()
                ret.update({
                    msg.FIELD_NAME: msg.TEST_SUCCESS
                })
                return Response(ret, status.HTTP_200_OK)
            else:
                ret.update({
                    code.FIELD_NAME: code.TEST_NONE,
                    msg.FIELD_NAME: msg.TEST_NONE
                })

        except Exception as e:
            print("..........................")
            ret.update({
                code.FIELD_NAME: code.TEST_FAIL,
                msg.FIELD_NAME: msg.TEST_FAIL
            })
            return Response(ret, status.HTTP_500_INTERNAL_SERVER_ERROR)


