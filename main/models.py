from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.


class Bicycle(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True, verbose_name='Nazwa roweru')
    desc = models.CharField(max_length=500, verbose_name='Opis roweru')
    cost = models.FloatField(null=False, verbose_name='Cena za godzinę')

    class Type(models.TextChoices):
        Górski = 'Górski'
        Szosowy = 'Szosowy'
        Turystyczny = 'Turystyczny'
        Inny = 'Inny'

    type = models.CharField(max_length=11, null=False, choices=Type.choices, default=Type.Górski,
                            verbose_name='Typ roweru')

    class Meta:
        verbose_name = 'Rower'
        verbose_name_plural = 'Rowery'

    def __str__(self):
        return self.name


class BicycleItem(models.Model):
    info = models.CharField(max_length=50, verbose_name='Informacje')
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE, related_name='bicycle_model', null=False,
                                verbose_name='Model')

    class Meta:
        verbose_name = 'Rower (sztuka)'
        verbose_name_plural = 'Rowery (sztuki)'

    def __str__(self):
        return str(self.bicycle) + ' (' + self.info + ')'
        # return self.info


class Rental(models.Model):
    start_time = models.DateTimeField(null=False, verbose_name='Czas od')
    end_time = models.DateTimeField(null=False, verbose_name='Czas do')
    num_hours = models.IntegerField(null=False, verbose_name='Liczba godzin')
    total_cost = models.FloatField(null=False, verbose_name='Łączny koszt')
    item = models.ForeignKey(BicycleItem, on_delete=models.CASCADE, related_name='rental_item', null=False,
                             verbose_name='Rower')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_client', null=False,
                               verbose_name='Klient')

    class Meta:
        verbose_name = 'Wypożyczenie'
        verbose_name_plural = 'Wypożyczenia'

    def __str__(self):
        return str(self.id) + '. ' + self.client.username + ', ' + str(self.item)


class Report(models.Model):
    text = models.CharField(max_length=500, null=False, verbose_name='treść zgłoszenia')
    date = models.DateField(default=date.today, verbose_name='data zgłoszenia')
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='report_rental', null=False,
                               verbose_name='Wypożyczenie')
    item = models.ForeignKey(BicycleItem, on_delete=models.CASCADE, related_name='report_item', null=False,
                             verbose_name='Rower')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_client', null=False,
                               verbose_name='Klient')

    class Meta:
        verbose_name = 'Zgłoszenie'
        verbose_name_plural = 'Zgłoszenia'

    def __str__(self):
        return self.client.username + ', ' + str(self.item)
