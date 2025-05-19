import django_filters
from django.contrib.auth.models import User 
from payment.models import Order
from django.db.models import Q

class UserFilter(django_filters.FilterSet):
    is_staff = django_filters.BooleanFilter(
        field_name='is_staff',
        label= "Is Staff"
    )
    
    is_superuser = django_filters.BooleanFilter(
        field_name= "is_superuser",
        label= "Is Superuser"
    )
    
    search = django_filters.CharFilter(
        method="filter_by_username",
        label="Search"
    )
    
    def filter_by_username(self,queryset,name, value):
        return queryset.filter(Q(username__icontains = value)| Q(id__icontains = value) | Q(email__icontains = value))
    
    class Meta:
        model = User 
        fields = []


class OrderFilter(django_filters.FilterSet):
    order_status = django_filters.ChoiceFilter(
        choices = Order.STATUS_ORDER,
        label='Order Status',
        empty_label="All Statuses",
        method='filter_by_status'
    )
    
    search = django_filters.CharFilter(
        method="custom_search",
        label="Search"
    )
    
    def filter_by_status(self,queryset, name, value):
        return queryset.filter(order_status = value)
    
    def custom_search(self,queryset,name, value):
        return queryset.filter(
            Q(user__username__icontains = value) |
            Q(id__icontains = value) |
            Q(invoice__icontains = value) |
            Q(payer_id__icontains = value)
        )
    
    class Meta:
        model = Order 
        fields = ['order_status']