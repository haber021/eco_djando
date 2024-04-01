# urls.py
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import get_user_info, upload_image_endpoint

app_name = 'bies'  # Define the app namespace

urlpatterns = [
    path('', views.index, name='index'),
    path('get_user_info/', get_user_info, name='get_user_info'),  
    path('logout/', views.logout, name='logout'),  
    path('add_expenses/', views.add_expenses, name='add_expenses'),  
    path('edit_data/<int:id>/', views.Edit_expenses, name='edit_data'),  
    path('delete_data/<int:id>/', views.delete_data, name='delete_data'),  
    path('search_expenses/', csrf_exempt(views.search_expenses), name='search_expenses'),
    path('upload_image/', upload_image_endpoint, name='upload_image'),
    # Define the URL pattern for image upload
    path('expense_category_summary/', views.expense_category_summary, name='expense_category_summary'),  # Corrected the name here
    path('stats/', views.stats_view, name='stats'),
    path('export_csv/', views.export_csv, name='export-csv'),
    path('export_excel/', views.export_excel, name='export-excel'),
    # path('export_pdf/', views.export_pdf, name='export-pdf'),
    path('expense_trend_over_time/', views.expense_trend_over_time, name='expense_trend_over_time'),  # Add the new endpoint here
    path('monthly_category_sales/', views.monthly_category_sales, name='monthly_category_sales'),

 
]