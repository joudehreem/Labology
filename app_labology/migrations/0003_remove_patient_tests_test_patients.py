# Generated by Django 5.0.7 on 2024-08-10 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_labology', '0002_rename_test_patient_tests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='tests',
        ),
        migrations.AddField(
            model_name='test',
            name='patients',
            field=models.ManyToManyField(related_name='tests', to='app_labology.patient'),
        ),
    ]