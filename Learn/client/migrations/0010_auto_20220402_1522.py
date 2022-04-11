# Generated by Django 3.2.9 on 2022-04-02 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_alter_bookapointment_user_booking_photographer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookapointment',
            name='user_booking_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.bookingcategories'),
        ),
        migrations.AlterField(
            model_name='bookapointment',
            name='user_booking_photographer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.photographers'),
        ),
    ]
