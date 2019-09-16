from django.db import models
from person.models import Person
from cdtTest.models import CdtTest


class File(models.Model):
    file_name = models.CharField(max_length=50)
    # file = models.FileField(upload_to='file/%Y/%m/%d/')
    file = models.FileField(upload_to='file/')
    file_url = models.URLField(max_length=255)
    test = models.ForeignKey(CdtTest, on_delete=models.CASCADE)

    class Meta:
        db_table = 'file'
