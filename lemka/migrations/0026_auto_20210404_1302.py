# Generated by Django 3.1.2 on 2021-04-04 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemka', '0025_auto_20210404_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devis',
            name='numero_devis',
            field=models.PositiveBigIntegerField(unique=True),
        ),
    ]
