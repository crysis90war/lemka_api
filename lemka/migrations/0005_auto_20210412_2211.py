# Generated by Django 3.1.2 on 2021-04-12 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lemka', '0004_auto_20210408_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demandedevis',
            old_name='ref_mercerie_option',
            new_name='ref_mercerie_options',
        ),
    ]
