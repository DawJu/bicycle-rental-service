# Generated by Django 3.2.8 on 2022-01-30 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_remove_bicycleitem_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rental_client', to=settings.AUTH_USER_MODEL, verbose_name='Klient'),
        ),
    ]