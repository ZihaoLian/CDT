from django.db import models
from cdtTest.models import CdtTest


class Person(models.Model):
    name = models.CharField(max_length=50, null=True)
    sex = models.BooleanField(default=0)
    age = models.PositiveIntegerField(max_length=4)
    unionId = models.CharField(primary_key=True, max_length=40)
    test = models.ForeignKey(CdtTest, on_delete=models.CASCADE)

    class Meta:
        db_table = 'person'


