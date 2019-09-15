from rest_framework.viewsets import ModelViewSet
from .serializer import ImageSerializer
from .models import Image
from cdtTest.models import CdtTest
from rest_framework.response import Response
from rest_framework import status
from public import code, msg, config
import time


# Create your views here.
class ImageView(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    def create(self, request, *args, **kwargs):
        ret = {
            code.FIELD_NAME: code.TEST_SUCCESS,
            msg.FIELD_NAME: None
        }

        image_name = request.data.get('fileName')
        image = request.FILES['image']   # 接收文件
        test_time = request.data.get('testTime')
        person = request.data.get('person')
        hand_time = request.data.get('handTime')

        image_url = config.BASE_URL + 'image/' + str(int(time.time())) + '_' + image.name

        try:
            if image_name is not None and image is not None and test_time is not None and person is not None:
                if not CdtTest.objects.get(person=person, test_time=test_time, hand_time=hand_time):
                    cdt_obj = CdtTest.objects.create(person=person, test_time=test_time, hand_time=hand_time)
                else:
                    cdt_obj = CdtTest.objects.get(person=person, test_time=test_time, hand_time=hand_time)
                if not Image.objects.get(image_name=image_name, image_url=image_url, test=cdt_obj.id):
                    Image.objects.create(image_name=image_name, image_url=image_url, test=cdt_obj.id)
                    ret.update({
                        msg.FIELD_NAME: msg.TEST_SUCCESS
                    })
                    return Response(ret, status.HTTP_200_OK)
                else:
                    ret.update({
                        code.FIELD_NAME: code.TEST_REPEAT,
                        msg.FIELD_NAME: msg.TEST_REPEAT
                    })
                    return Response(ret)
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
