import django_filters
from .models import *

class UserIncomeFilter(django_filters.FilterSet):
    class Meta:
        model = UserIncome
        fields = '__all__'