# Generated by Django 2.0.3 on 2018-03-30 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('npl', '0004_auto_20180330_1602'),
    ]

    operations = [
        migrations.RenameField(
            model_name='encounter',
            old_name='street_address',
            new_name='street_address_name',
        ),
        migrations.AddField(
            model_name='encounter',
            name='street_address_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
