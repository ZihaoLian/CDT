from django.db import models
from person.models import Person


class Image(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='img/%Y/%m/%d/')
    testTime = models.DateTimeField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        db_table = 'image'

