import django_filters
from .models import Store

class StoreFilter(django_filters.FilterSet):
    product_price = django_filters.RangeFilter()

    class Meta:
        model = Store
        fields = {
            'category':['exact'],
            'product_price':['gt', 'lt']
        }