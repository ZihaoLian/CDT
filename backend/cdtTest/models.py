from django.db import models
from file.models import File
from image.models import Image


class CdtTest(models.Model):
    testTime = models.DateTimeField()
    handTime = models.TimeField()
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cdtTest'

