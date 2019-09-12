from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=100)

    class Meta:
        db_table = 'image'

