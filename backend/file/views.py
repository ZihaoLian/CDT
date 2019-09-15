from rest_framework.viewsets import ModelViewSet
from .serializer import FileSerializer
from .models import File
from cdtTest.models import CdtTest
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
        file = request.FILES['file']   # 接收文件
        test_time = request.data.get('testTime')
        person = request.data.get('person')
        hand_time = request.data.get('handTime')

        file_url = config.BASE_URL + 'file/' + str(int(time.time())) + '_' + file.name
        try:
            if file_name is not None and file is not None and test_time is not None and person is not None:
                cdt_obj = CdtTest(test_time=test_time, hand_time=hand_time, person=person)
                cdt_obj.save()
                print('shg')
                # cdt_obj = CdtTest.objects.create(person=person, test_time=test_time, hand_time=hand_time)

                # File.objects.create(file_name=file_name, file_url=file_url, test=cdt_obj.id)
                # ret.update({
                #     msg.FIELD_NAME: msg.TEST_SUCCESS
                # })
                # return Response(ret, status.HTTP_200_OK)
            else:
                ret.update({
                    code.FIELD_NAME: code.TEST_NONE,
                    msg.FIELD_NAME: msg.TEST_NONE
                })

        except Exception as e:
            ret.update({
                code.FIELD_NAME: code.TEST_FAIL,
                msg.FIELD_NAME: msg.TEST_FAIL
            })
            return Response(ret, status.HTTP_500_INTERNAL_SERVER_ERROR)


