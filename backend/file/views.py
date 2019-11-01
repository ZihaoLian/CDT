from rest_framework.viewsets import ModelViewSet
from .serializer import FileSerializer
from .models import File
from cdtTest.models import CdtTest
from rest_framework.response import Response
from rest_framework import status
from public import code, msg, config
from image.models import Image
from cdtTest.serializer import CdtTestSerializer
from image.serializer import ImageSerializer
from file.cdt.test import CDT


# Create your views here.
class FileView(ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()

    def create(self, request, *args, **kwargs):
        CDT.detect("../cdt/73471568716181723_1.csv", "../cdt/73471568716181723_2.csv", 3, 25)
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
        id_x = request.data.get('idx')

        # try:
        if file_name is not None and file is not None and test_time is not None and person is not None:
            # try:
            #     file_name = 'origin'
            #     cdt_obj = CdtTest.objects.get(test_time=test_time, hand_time=hand_time, person_id=person)
            # except CdtTest.DoesNotExist:
            #     file_name = 'copy'
            #     cdt_obj = CdtTest(test_time=test_time, hand_time=hand_time, person_id=person, result=0)
            # cdt_obj.save()
            if id_x == '1':
                file_name = 'origin'
            else:
                file_name = 'copy'

            cdt_obj = CdtTest.objects.get(test_time=test_time, hand_time=hand_time, person_id=person)

            file_obj = File(file=file)
            file_obj.file_name = file_name
            file_obj.test_id = cdt_obj.id
            file_obj.file_url = file_url
            file_obj.save()
            ret.update({
                msg.FIELD_NAME: msg.TEST_SUCCESS,
            })

            img_obj = Image.objects.get(test_id=file_obj.test_id, image_name=file_name)
            img_obj = ImageSerializer(instance=img_obj).data
            ret.update({
                'img': img_obj,
                'result': cdt_obj.result,
                'handTime': cdt_obj.hand_time,
                'testTime': cdt_obj.test_time
            })
            # try:
            #     with open("file/1.png", 'rb') as f:
            #         contents = f.read()
            #         # img = Image(image=contents)
            #         img = Image(image=contents)
            #         # img.image.save('filename.png', contents, True)
            #         img.image_name = '测试'
            #         img.image_url = 'http://127.0.0.1:8000/api/v1/file/media/img/1b701568621219604_1.docx'
            #         img.test_id = cdt_obj.id
            #         img.save()
            # except Exception as e:
            #     print(e)

            return Response(ret, status.HTTP_200_OK)
        else:
            ret.update({
                code.FIELD_NAME: code.TEST_NONE,
                msg.FIELD_NAME: msg.TEST_NONE
            })
            return  Response(ret)

        # except Exception as e:
        #     ret.update({
        #         code.FIELD_NAME: code.TEST_FAIL,
        #         msg.FIELD_NAME: msg.TEST_FAIL
        #     })
        #     return Response(ret, status.HTTP_500_INTERNAL_SERVER_ERROR)


