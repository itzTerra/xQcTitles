# Generated by Django 3.1.4 on 2020-12-21 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
            ],
        ),
    ]
