# Generated by Django 5.1.1 on 2024-11-01 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appli_ParcourSup', '0008_formation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formation',
            name='image',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
