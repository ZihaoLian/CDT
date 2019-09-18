from rest_framework.viewsets import ModelViewSet
from .serializer import ImageSerializer
from .models import Image
from cdtTest.models import CdtTest
from rest_framework.response import Response
from rest_framework import status
from public import code, msg, config


# Create your views here.
class ImageView(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    # def retrieve(self, request, *args, **kwargs):
    #     ret = {
    #         code.FIELD_NAME: code.IMAGE_FAIL,
    #         msg.FIELD_NAME: msg.IMAGE_FAIL,
    #     }
    #     try:
    #         path = kwargs.get('path', None)
    #         # (1) check if we get the path
    #         if not path:
    #             ret.update({
    #                 code.FIELD_NAME: code.IMAGE_PATH_NOT_FOUND,
    #                 msg.FIELD_NAME: msg.IMAGE_PATH_NOT_FOUND
    #             })
    #             return Response(ret, status.HTTP_404_NOT_FOUND)
    #
    #         # (2) check file exist
    #         path = os.path.join(config.BASE_URL, path)
    #         print(path)
    #         if not os.path.exists(path):
    #             ret.update({
    #                 code.FIELD_NAME: code.IMAGE_NOT_EXIST,
    #                 msg.FIELD_NAME: msg.IMAGE_NOT_EXIST
    #             })
    #             return Response(ret, status.HTTP_404_NOT_FOUND)
    #         print(path)
    #         with open(path, 'rb') as f:
    #             contents = f.read()
    #
    #         return Response(contents, content_type='image/png')
    #
    #     except Exception as e:
    #         print('In Image View, unexpected error occurs, exception type `%s.`' % str(type(e)))
    #         ret.update({
    #             code.FIELD_NAME: code.IMAGE_UNEXPECTED_ERROR,
    #             msg.FIELD_NAME: msg.IMAGE_UNEXPECTED_ERROR
    #         })
    #         return Response(ret, status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        id_x = request.data.get('idx')
        image_url = config.BASE_URL + 'img/' + image.name

        try:
            if image_name is not None and image is not None and test_time is not None and person is not None:
                try:
                    image_name = 'origin'
                    cdt_obj = CdtTest.objects.get(test_time=test_time, hand_time=hand_time, person_id=person)
                except CdtTest.DoesNotExist:
                    image_name = 'copy'
                    cdt_obj = CdtTest(test_time=test_time, hand_time=hand_time, person_id=person, result=0)
                cdt_obj.save()

                cdt_obj = CdtTest.objects.get(test_time=test_time, hand_time=hand_time, person_id=person)

                image_obj = Image(image=image)
                image_obj.image_name = image_name
                image_obj.test_id = cdt_obj.id
                image_obj.image_url = image_url
                image_obj.save()
                ret.update({
                    msg.FIELD_NAME: msg.TEST_SUCCESS
                })
                return Response(ret, status.HTTP_200_OK)
            else:
                ret.update({
                    code.FIELD_NAME: code.TEST_NONE,
                    msg.FIELD_NAME: msg.TEST_NONE
                })
                return Response(ret, status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            ret.update({
                code.FIELD_NAME: code.TEST_FAIL,
                msg.FIELD_NAME: msg.TEST_FAIL
            })
            return Response(ret, status.HTTP_500_INTERNAL_SERVER_ERROR)
