from django.db import models
from person.models import Person


class CdtTest(models.Model):
    test_time = models.DateTimeField()
    hand_time = models.TimeField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        # unique_together = ("testTime", "person")  # 让testTime和person同时作为主键
        db_table = 'cdtTest'
