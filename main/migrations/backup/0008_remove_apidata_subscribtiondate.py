# Generated by Django 3.1.4 on 2021-09-26 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_delete_accesstoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apidata',
            name='subscribtionDate',
        ),
    ]
