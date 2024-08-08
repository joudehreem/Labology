# Generated by Django 5.0.7 on 2024-08-06 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=50)),
                ('clinic', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=225)),
                ('password', models.CharField(max_length=225)),
                ('confirm_password', models.CharField(max_length=225)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_test', models.CharField(choices=[('IRON', 'Iron'), ('VITAMIN_D', 'Vitamin D')], max_length=20)),
                ('test_result', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('mobile', models.CharField(max_length=255)),
                ('id_number', models.CharField(blank=True, max_length=255)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=20)),
                ('description', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('episodes', models.ManyToManyField(related_name='patients', to='app_labology.provider')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_labology.test')),
            ],
        ),
    ]
