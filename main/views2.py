from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters import NumberFilter, DateTimeFilter, BooleanFilter
from django_filters.rest_framework import FilterSet
from rest_framework import permissions
from django.contrib.auth.models import User
from .models import *
from .serializers import *


class RootApi(generics.GenericAPIView):
    name = 'root-api'

    def get(self, request, *args, **kwargs):
        return Response({
            'bicycles': reverse(BicycleList.name, request=request),
            'bicycle_items': reverse(BicycleItemList.name, request=request),
            'rentals': reverse(RentalList.name, request=request),
            'reports': reverse(ReportList.name, request=request),
            'users': reverse(UserList.name, request=request),
        })


class BicycleFilter(FilterSet):
    min_cost = NumberFilter(field_name='cost', lookup_expr='gte')
    max_cost = NumberFilter(field_name='cost', lookup_expr='lte')

    class Meta:
        model = Bicycle
        fields = ['name', 'type', 'min_cost', 'max_cost']


class BicycleList(generics.ListCreateAPIView):
    queryset = Bicycle.objects.all()
    serializer_class = BicycleSerializer
    name = 'bicycle-list'
    filter_class = BicycleFilter
    search_fields = ['name', 'desc', 'type']
    ordering_fields = ['name', 'cost']
    permission_classes = [permissions.IsAdminUser]


class BicycleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bicycle.objects.all()
    serializer_class = BicycleSerializer
    name = 'bicycle-detail'
    permission_classes = [permissions.IsAdminUser]


class BicycleItemList(generics.ListCreateAPIView):
    queryset = BicycleItem.objects.all()
    serializer_class = BicycleItemSerializer
    name = 'bicycle-item-list'
    search_fields = ['bicycle', 'info']
    ordering_fields = ['bicycle', 'info']
    permission_classes = [permissions.IsAdminUser]


class BicycleItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BicycleItem.objects.all()
    serializer_class = BicycleItemSerializer
    name = 'bicycleitem-detail'
    permission_classes = [permissions.IsAdminUser]


class RentalFilter(FilterSet):
    from_start_time = DateTimeFilter(field_name='start_time', lookup_expr='gte')
    to_start_time = DateTimeFilter(field_name='start_time', lookup_expr='lte')
    from_end_time = DateTimeFilter(field_name='end_time', lookup_expr='gte')
    to_end_time = DateTimeFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = Rental
        fields = ['from_start_time', 'to_start_time', 'from_end_time', 'to_end_time']


class RentalList(generics.ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    name = 'rental-list'
    filter_class = RentalFilter
    ordering_fields = ['start_time', 'end_time', 'num_hours', 'total_cost']
    permission_classes = [permissions.IsAdminUser]


class RentalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    name = 'rental-detail'
    permission_classes = [permissions.IsAdminUser]


class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    name = 'report-list'
    search_fields = ['text']
    ordering_fields = ['id']
    permission_classes = [permissions.IsAdminUser]


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    name = 'report-detail'
    permission_classes = [permissions.IsAdminUser]


class UserFilter(FilterSet):
    is_staff = BooleanFilter(field_name='is_staff')
    is_superuser = BooleanFilter(field_name='is_superuser')


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
    filter_class = UserFilter
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'first_name', 'last_name']
    permission_classes = [permissions.IsAdminUser]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
    permission_classes = [permissions.IsAdminUser]
