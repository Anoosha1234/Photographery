# Generated by Django 3.2.9 on 2022-02-26 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_alter_bookapointment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_password',
            field=models.CharField(max_length=30),
        ),
    ]
