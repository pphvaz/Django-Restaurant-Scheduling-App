# Generated by Django 4.2.7 on 2023-12-23 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chefiapp', '0017_monthlyschedule_year'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monthlyschedule',
            unique_together={('user', 'month', 'year')},
        ),
    ]
