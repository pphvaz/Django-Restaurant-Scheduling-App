# Generated by Django 4.2.7 on 2023-12-10 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chefiapp', '0004_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateField(blank=True, null=True, verbose_name='date joined'),
        ),
    ]
