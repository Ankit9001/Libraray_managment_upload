# Generated by Django 4.2.2 on 2023-09-23 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_given',
            field=models.CharField(blank=True, default='n', max_length=2, null=True),
        ),
    ]
