from django.db import models
from person.models import Person
from cdtTest.models import CdtTest


class Image(models.Model):
    image_name = models.CharField(max_length=50)
    # image = models.ImageField(upload_to='img/%Y/%m/%d/')
    image_url = models.ImageField(upload_to='img/')
    test = models.ForeignKey(CdtTest, on_delete=models.CASCADE)

    class Meta:
        db_table = 'image'


