from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from public import code, msg
from image.models import Image
from image.serializer import ImageSerializer
from .serializer import CdtTestSerializer
from .models import CdtTest


# Create your views here.
class CdtTestView(ModelViewSet):
    serializer_class = CdtTestSerializer
    queryset = CdtTest.objects.all()

    def list(self, request, *args, **kwargs):
        ret = {
            code.FIELD_NAME: code.DETAIL_SUCCESS,
            msg.FIELD_NAME: None
        }

        detail_list = []

        person = kwargs.get('openId', None)
        # person = request.data.get('person')
        if person is not None:
            try:
                cdt_test_list = CdtTest.objects.filter(person=person)
                if cdt_test_list.exists():
                    # cdt_test_ser = CdtTestSerializer(instance=cdt_test_list, many=True).data
                    for item in cdt_test_list:
                        test_dict = {}
                        try:
                            image_list = Image.objects.filter(test_id=item.id)
                            image_ser = ImageSerializer(instance=image_list, many=True).data
                            for image in image_ser:
                                if image['image_name'] == 'copy':
                                    test_dict['copy'] = image
                                else:
                                    test_dict['first'] = image

                            test_dict['testTime'] = item.test_time
                            test_dict['handTime'] = item.hand_time
                            detail_list.append(test_dict)
                            ret.update({
                                'detail_list': detail_list
                            })

                        except Image.DoesNotExist:
                            ret.update({
                                code.FIELD_NAME: code.DETAIL_NO_IMAGE,
                                msg.FIELD_NAME: msg.DETAIL_NO_IMAGE
                            })
                            return Response(ret, status.HTTP_404_NOT_FOUND)

                    ret.update({
                        msg.FIELD_NAME: msg.DETAIL_SUCCESS
                    })
                    return Response(ret)
                else:
                    ret.update({
                        code.FIELD_NAME: code.DETAIL_NO_IMAGE,
                        msg.FIELD_NAME: msg.DETAIL_NO_IMAGE
                    })
                    return Response(ret, status.HTTP_204_NO_CONTENT)
            except Exception:
                ret.update({
                    code.FIELD_NAME: code.DETAIL_FAIL,
                    msg.FIELD_NAME: msg.DETAIL_FAIL
                })

        else:
            ret.update({
                code.FIELD_NAME: code.DETAIL_NO_PERSON,
                msg.FIELD_NAME: msg.DETAIL_NO_PERSON
            })
            return Response(ret, status.HTTP_403_FORBIDDEN)
            