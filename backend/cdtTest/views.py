from rest_framework.viewsets import ModelViewSet
from .serializer import CdtTestSerializer
from .models import CdtTest
from public import code, msg
from image.models import Image


# Create your views here.
class CdtTestView(ModelViewSet):
    serializer_class = CdtTestSerializer
    queryset = CdtTest.objects.all()

    def list(self, request, *args, **kwargs):
        ret = {
            code.FIELD_NAME: code.TEST_SUCCESS,
            msg.FIELD_NAME: None
        }
        # test_time = models.DateTimeField()
        # hand_time = models.TimeField()
        # person = models.ForeignKey(Person, on_delete=models.CASCADE)
        #
        # person = request.data.get('person')
        # test_list = CdtTest.objects.filter(person=person)
        # test_list = CdtTestSerializer(test_list).data
        # for item in test_list:
        #     print()



    # def create(self, request, *args, **kwargs):
    #     ret = dict(code=code.TEST_SUCCESS)
    #     test_time = request.data.get('testTime')
    #     hand_time = request.data.get('handTime')
    #     person = request.data.get('handTime')
    #
    #     file_url = models.FileField(upload_to='file/')
    #     test = models.ForeignKey(CdtTest, on_delete=models.CASCADE)
    #
    #     file_name = str(int(time.time())) + '_' + file.name
    #
    #     if person is not None and test_time is not None and person is not None:
    #         test_obj = CdtTest.objects.create(test_time=test_time, hand_time=hand_time, person=person)
    #         file_obj = File.objects.create(file_url=(config.BASE_URL + 'file/' + ))
    #         print(test_obj.id)










