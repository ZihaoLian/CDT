# Generated by Django 2.2.5 on 2019-09-15 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cdtTest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=50)),
                ('file_url', models.FileField(upload_to='file/')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cdtTest.CdtTest')),
            ],
            options={
                'db_table': 'file',
            },
        ),
    ]
