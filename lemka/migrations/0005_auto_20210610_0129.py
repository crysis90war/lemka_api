# Generated by Django 3.1.8 on 2021-06-10 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemka', '0004_auto_20210609_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(editable=False, max_length=255, unique=True),
        ),
    ]
