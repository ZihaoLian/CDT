# Generated by Django 2.2.2 on 2019-09-16 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cdtTest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='img/')),
                ('image_url', models.URLField(max_length=255)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cdtTest.CdtTest')),
            ],
            options={
                'db_table': 'image',
            },
        ),
    ]
