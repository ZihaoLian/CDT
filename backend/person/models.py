from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50, null=True)
    sex = models.BooleanField(default=0)
    age = models.PositiveIntegerField(null=True)
    openId = models.CharField(primary_key=True, max_length=40)

    class Meta:
        db_table = 'person'
