# Generated by Django 3.1.4 on 2020-12-26 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_accesstoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='category',
            field=models.CharField(default='category', max_length=255),
            preserve_default=False,
        ),
    ]
