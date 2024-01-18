# Generated by Django 4.2.7 on 2023-12-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chefiapp', '0007_remove_user_department_abilities'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('pizzaiolo', 'Pizzaiolo'), ('estafeta', 'Estafeta'), ('caixa', 'Caixa'), ('gerente', 'Gerente')], max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='departments',
            field=models.ManyToManyField(blank=True, related_name='users', to='chefiapp.department'),
        ),
    ]