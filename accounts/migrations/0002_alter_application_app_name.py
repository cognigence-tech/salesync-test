# Generated by Django 5.0.2 on 2024-10-05 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='app_name',
            field=models.CharField(max_length=255),
        ),
    ]