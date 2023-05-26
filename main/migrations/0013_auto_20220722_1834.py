# Generated by Django 3.2.5 on 2022-07-22 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_duplicatefilter'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('entryIDs', models.JSONField(default=dict)),
                ('lastChanged', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='DuplicateFilter',
        ),
    ]