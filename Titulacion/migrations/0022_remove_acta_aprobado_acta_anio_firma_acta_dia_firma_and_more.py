# Generated by Django 5.1.2 on 2025-05-27 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Titulacion', '0021_acta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acta',
            name='Aprobado',
        ),
        migrations.AddField(
            model_name='acta',
            name='anio_firma',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='acta',
            name='dia_firma',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='acta',
            name='foja',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='acta',
            name='libro',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='acta',
            name='mes_firma',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
