# Generated by Django 3.1.4 on 2021-11-23 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20210926_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='apidata',
            name='verificationSecret',
            field=models.CharField(default='0', max_length=255),
        ),
    ]