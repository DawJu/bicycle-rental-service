# Generated by Django 3.2.8 on 2022-01-28 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_report_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bicycleitem',
            name='is_available',
        ),
    ]
