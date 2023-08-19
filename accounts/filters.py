import django_filters
from django_filters import DateFilter, CharFilter


from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_updated', lookup_expr='lte')
    description = CharFilter(field_name='description', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer','date_created','date_updated']