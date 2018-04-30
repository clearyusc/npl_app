# Generated by Django 2.0.2 on 2018-03-30 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('npl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='apt_or_unit',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='street_address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='npl.Laborer'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='zip',
            field=models.IntegerField(blank=True, null=models.BooleanField(default=False)),
        ),
    ]