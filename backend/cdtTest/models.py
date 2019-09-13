from django.db import models
from person.models import Person


class CdtTest(models.Model):
    testTime = models.DateTimeField()
    handTime = models.TimeField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        # unique_together = ("testTime", "person")  # 让testTime和person同时作为主键
        db_table = 'cdtTest'
