# Generated by Django 5.0.2 on 2024-10-05 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_application_app_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='application',
            constraint=models.UniqueConstraint(fields=('app_name', 'country'), name='unique_app_name_country'),
        ),
    ]
