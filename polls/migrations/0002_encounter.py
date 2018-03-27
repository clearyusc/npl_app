# Generated by Django 2.0.2 on 2018-03-18 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('response', models.CharField(choices=[('RL', 'Red Light'), ('YL', 'Yellow Light'), ('GL', 'Green Light'), ('WT', 'Believer Wants Training'), ('RT', 'Believer Rejects Training')], max_length=2)),
                ('notes', models.TextField()),
                ('date_time', models.DateTimeField()),
            ],
        ),
    ]
