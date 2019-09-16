from django.db import models
from person.models import Person
from cdtTest.models import CdtTest


class Image(models.Model):
    image_name = models.CharField(max_length=50)
    # image = models.ImageField(upload_to='img/%Y/%m/%d/')
    image = models.ImageField(upload_to='img/')
    image_url = models.URLField(max_length=255)
    test = models.ForeignKey(CdtTest, on_delete=models.CASCADE)

    class Meta:
        db_table = 'image'


