# Generated by Django 5.1.3 on 2025-01-29 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh_personal', '0006_alter_certificacion_rutadoc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examen',
            name='rutaDoc',
            field=models.FileField(upload_to='Examenes'),
        ),
    ]
