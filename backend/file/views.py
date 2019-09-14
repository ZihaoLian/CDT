from rest_framework.viewsets import ModelViewSet
from .serializer import FileSerializer
from .models import File
from person.models import Person
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class FileView(ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()

    # def create(self, request, *args, **kwargs):
    #     ret = {'code': 1000, 'msg': None}
    #     name = request.data.get('name')
    #     file = request.FILES['file']
    #     testTime = request.data.get('testTime')
    #     person = request.data.get('person')
    #
    #     if person is not None and name is not None and file is not None and testTime is not None:
    #         try:
    #             person = Person.objects.get(openId=person)
    #             if person is not None and not File.objects.get(name=name, testTime=testTime):
    #                 File.objects.create(name=name, file=file, testTime=testTime, person=person)
    #                 ret['msg'] = '成功获取文件'
    #                 return Response(ret)
    #             else:
    #                 ret['msg'] = '获取文件失败'
    #                 ret['code'] = 1001
    #                 return Response(ret)
    #         except Exception as e:
    #             return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     else:
    #         ret['code'] = 1002
    #         ret['msg'] = '请检查文件名，文件，测试时间，人员是否准确'
    #         return Response(ret)

