# Generated by Django 5.1.2 on 2024-11-27 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Titulacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='titulacion',
            name='carrera',
            field=models.CharField(choices=[('INGENIERÍA BIOQUÍMICA', 'INGENIERÍA BIOQUÍMICA'), ('INGENIERÍA CIVIL', 'INGENIERÍA CIVIL')], default='INGENIERÍA BIOQUÍMICA', max_length=100),
        ),
    ]
