# Generated by Django 3.1.8 on 2021-06-10 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lemka', '0006_remove_article_ref_catalogue'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Catalogue',
        ),
    ]
