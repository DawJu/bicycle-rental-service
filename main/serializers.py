from rest_framework import serializers
from .models import *


class BicycleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bicycle
        fields = ['url', 'id', 'name', 'desc', 'cost', 'type']


class BicycleItemSerializer(serializers.HyperlinkedModelSerializer):
    bicycle = serializers.SlugRelatedField(queryset=Bicycle.objects.all(), slug_field='name', label='Model')

    class Meta:
        model = BicycleItem
        fields = ['url', 'id', 'bicycle', 'info']


class RentalSerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.SlugRelatedField(queryset=BicycleItem.objects.all(), slug_field='id', label='Rower')
    client = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', label='Klient')

    class Meta:
        model = Rental
        fields = ['url', 'id', 'item', 'client', 'start_time', 'end_time', 'num_hours', 'total_cost']


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.SlugRelatedField(queryset=BicycleItem.objects.all(), slug_field='id', label='Rower')
    client = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username', label='Klient')

    class Meta:
        model = Report
        fields = ['url', 'id', 'rental', 'item', 'client', 'text', 'date']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff']
