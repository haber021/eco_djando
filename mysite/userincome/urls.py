
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


app_name = 'income'  # Define the app namespace


urlpatterns = [
    path('', views.index, name='index'),  
    path('add_income/', views.add_income, name='add_income'),  
    path('edit_data/<int:id>/', views.Edit_Income, name='edit_data'),  
    path('delete_data/<int:id>/', views.delete_data, name='delete_data'),  
    path('search_incomes/', csrf_exempt(views.search_incomes), name='search_incomes'),
    path('user_income_list/', views.user_income_list, name='user_income_list'),  # Corrected URL mapping
    path('income_trend_over_time/', views.income_trend_over_time, name='income_trend_over_time'),  # Corrected URL mapping
    path('last_month_income/', views.last_month_income, name='last_month_income'),  # Corrected URL mapping
    # path('custom_date_range_income/', views.custom_date_range_income, name='custom_date_range_income'),  # Corrected URL mapping
    path('income_list/', views.income_list, name='income_list'),  # Corrected URL mapping
]