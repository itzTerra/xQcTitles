# Generated by Django 3.2.5 on 2022-07-02 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_apidata_verificationsecret'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuplicateFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entryIDs', models.JSONField(default=dict)),
                ('lastChanged', models.DateTimeField()),
            ],
        ),
    ]