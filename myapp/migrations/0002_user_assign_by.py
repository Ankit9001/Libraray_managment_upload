# Generated by Django 4.1.5 on 2023-09-22 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='assign_by',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
