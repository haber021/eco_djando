
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from .models import Category, Expense
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
import json
from django.utils.dateparse import parse_date

from userpreferences.models import UserPreferences
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
import os
from django.conf import settings
from django.http import JsonResponse


import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string





import xlwt
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0

    front_style = xlwt.XFStyle()
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category__name', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


import csv
def export_csv(request):

    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Expenses'+ \
        str(datetime.datetime.now())+'.csv'

    writer=csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])


    return response






def stats_view(request):
    return render(request, 'bies/stats.html')


import datetime
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from .models import Expense

def monthly_category_sales(request):
    today = datetime.date.today()
    six_months_ago = today - datetime.timedelta(days=30 * 6)

    # Group expenses by category and month, and calculate the total amount for each group
    expenses = Expense.objects.filter(
        owner=request.user,
        date__gte=six_months_ago,
        date__lte=today
    ).annotate(
        month=TruncMonth('date')
    ).values('category__name', 'month').annotate(
        total_amount=Sum('amount')
    )

    # Create a dictionary to store the category-wise monthly sales
    category_data = {}
    for expense in expenses:
        category_name = expense['category__name']
        month = expense['month'].strftime('%Y-%m')  # Format the month as YYYY-MM
        total_amount = expense['total_amount']

        if category_name not in category_data:
            category_data[category_name] = {}

        category_data[category_name][month] = total_amount

    return JsonResponse({'monthly_category_sales': category_data})




#endpoint line chart
import datetime
from django.http import JsonResponse
from .models import Expense
from sklearn.neighbors import KNeighborsRegressor

import datetime
from django.http import JsonResponse
from .models import Expense
from sklearn.neighbors import KNeighborsRegressor

def expense_trend_over_time(request):
    today = datetime.date.today()

    expenses = Expense.objects.filter(owner=request.user, date=today)

    today_sales = {}
    for expense in expenses:
        category_name = expense.category.name
        today_sales[category_name] = today_sales.get(category_name, 0) + expense.amount

    return JsonResponse({'expense_trend_data': {'today': today_sales}})

#endpoint for the dounut
import datetime
def expense_category_summary(request):
    today = datetime.date.today()
    six_months_ago = today - datetime.timedelta(days=30 * 6)

    expenses = Expense.objects.filter(owner=request.user,
                                       date__gte=six_months_ago, date__lte=today)

    category_data = {}
    for expense in expenses:
        category_name = expense.category.name
        category_data[category_name] = category_data.get(category_name, 0) + expense.amount

    return JsonResponse({'expense_category_data': category_data})





def upload_image_endpoint(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        # Specify the path to save the image
        image_path = os.path.join(settings.STATIC_ROOT, 'img', image_file.name)
        # Save the image file to the specified location
        with open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        # Respond with success message
        return JsonResponse({'success': True})
    else:
        # No image file found in the request
        return JsonResponse({'error': 'No image file found'}, status=400)
    



    
def get_user_info(request):
    email = request.GET.get('email')
    try:
        user = User.objects.get(email=email)
        user_info = {
            'username': user.username,
            'email': user.email,
            # Add more fields as needed
        }
        return JsonResponse({'user_info': user_info})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


#search bar backend
from .models import Expense  # Import the Expense model

from django.db.models import Q

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            Q(amount__istartswith=search_str) |
            Q(date__icontains=search_str) |
            Q(description__icontains=search_str) |
            Q(category__name__icontains=search_str),
            owner=request.user
        )
        data = [
            {
                'amount': expense.amount,
                'expense': expense.category.name if expense.category else "Uncategorized",
                'description': expense.description,
                'date': expense.date.strftime('%Y-%m-%d')  # Format date as needed
            }
            for expense in expenses
        ]
        return JsonResponse(data, safe=False)






@login_required(login_url='/authentication/login/')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    try:
        user_preferences = UserPreferences.objects.get(user=request.user)
        currency = user_preferences.currency
    except UserPreferences.DoesNotExist:
        currency = None
    
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'bies/index.html', context)

@login_required(login_url='/authentication/login/')
def logout(request):
    if not request.session.get('refreshed', False):
        request.session['refreshed'] = True
        django_logout(request)
        # Redirect to the home page after a delay of 3 seconds (3000 milliseconds)
        return redirect('bies:index')  # Corrected redirection to 'expenses:index'
    else:
        # Redirect to the login page if already refreshed
        return redirect('authentication:login')

@login_required(login_url='/authentication/login/')
def add_expenses(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('expense_date')
        category_name = request.POST.get('category')  # Get the category name from the form

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'bies/add_expenses.html', context)

        if not amount.isdigit():
            messages.error(request, 'Amount should be a number')
            return render(request, 'bies/add_expenses.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'bies/add_expenses.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'bies/add_expenses.html', context)

        if not category_name:
            messages.error(request, 'Category is required')
            return render(request, 'bies/add_expenses.html', context)

        try:
            # Get the Category instance based on the name provided in the form
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category')
            return render(request, 'bies/add_expenses.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date, 
                               category=category, description=description)
        
        messages.success(request, 'Expense saved successfully')

        return redirect('bies:index')  # Redirect to the index view of expenses app

    return render(request, 'bies/add_expenses.html', context)



#edit
def Edit_expenses(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
    }

    if request.method == 'GET':
        return render(request, 'bies/edit_data.html', context)
    
    elif request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('expense_date')
        category_name = request.POST.get('category')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'bies/edit_data.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'bies/edit_data.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'bies/edit_data.html', context)

        if not category_name:
            messages.error(request, 'Category is required')
            return render(request, 'bies/edit_data.html', context)

        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category')
            return render(request, 'bies/edit_data.html', context)

        # Update the expense object with the new values
        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.category = category
        expense.save()

        messages.success(request, 'Expense updated successfully')

        return redirect('bies:index')

#delete
from django.shortcuts import get_object_or_404

def delete_data(request, id):
    expense = get_object_or_404(Expense, pk=id)
    expense.delete()
    messages.success(request, 'Expense removed successfully')
    return redirect('bies:index')
