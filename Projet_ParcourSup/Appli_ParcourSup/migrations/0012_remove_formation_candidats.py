# Generated by Django 5.1.1 on 2024-11-06 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Appli_ParcourSup', '0011_candidature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formation',
            name='candidats',
        ),
    ]
