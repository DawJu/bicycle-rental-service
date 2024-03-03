# Generated by Django 3.2.8 on 2022-01-27 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220125_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='BicycleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(max_length=50, verbose_name='Informacje')),
                ('is_available', models.BooleanField(default=True, verbose_name='Dostępny')),
                ('bicycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bicycle_model', to='main.bicycle', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Rower (sztuka)',
                'verbose_name_plural': 'Rowery (sztuki)',
            },
        ),
    ]