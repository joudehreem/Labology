# Generated by Django 5.0.7 on 2024-08-11 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_labology', '0004_remove_test_patients_patienttest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='test_result',
        ),
        migrations.AddField(
            model_name='patienttest',
            name='test_result',
            field=models.FloatField(blank=True, null=True),
        ),
    ]