# Generated by Django 3.1.4 on 2021-07-17 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_entry_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessToken', models.CharField(max_length=255)),
                ('accessTokenExpireDate', models.DateTimeField()),
                ('subscribtionDate', models.DateTimeField()),
            ],
        ),
    ]
