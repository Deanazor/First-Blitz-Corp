# Generated by Django 2.2.14 on 2020-11-19 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20201119_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='delivery_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Address'),
        ),
    ]
