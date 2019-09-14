from django.db import models
from person.models import Person


class File(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='file/%Y/%m/%d/')
    testTime = models.DateTimeField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        db_table = 'file'
        # unique_together = ("testTime", "person", "name")  # 让testTime和person同时作为主键
