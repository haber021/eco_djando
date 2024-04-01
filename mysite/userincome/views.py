from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import Q




# views.py
from django.shortcuts import render
from .models import UserIncome
from .filters import UserIncomeFilter

def income_list(request):
    # Retrieve all income objects
    incomes = UserIncome.objects.all()
    
    # Initialize the filter
    myfilter = UserIncomeFilter(request.GET, queryset=incomes)
    incomes = myfilter.qs
    
    context = {'incomes': incomes, 'myFilter': myfilter}

    # Render the template with the filtered queryset and filter form
    return render(request, 'income/index.html', context)



from datetime import date, timedelta
from django.http import JsonResponse
from .models import UserIncome

def last_month_income(request):
    try:
        # Calculate the date range for the last month
        today = date.today()
        last_month_start = today.replace(day=1) - timedelta(days=1)  # Last day of previous month
        last_month_end = today  # Current day

        # Retrieve user income records for the last month
        incomes = UserIncome.objects.filter(owner=request.user,
                                             date__gte=last_month_start,
                                             date__lte=last_month_end)

        # Calculate income data for the last month
        income_data = {}
        for income in incomes:
            source_name = income.source.name
            income_data[source_name] = income_data.get(source_name, 0) + income.amount

        return JsonResponse({'last_month_income': income_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




def income_trend_over_time(request):
    today = datetime.date.today()

    incomes = UserIncome.objects.filter(owner=request.user, date=today)

    today_sales = {}
    for income in incomes:
        source_name = income.source.name
        today_sales[source_name] = today_sales.get(source_name, 0) + income.amount

    return JsonResponse({'income_trend_data': {'today': today_sales}})




import datetime
from django.http import JsonResponse
from .models import UserIncome

def user_income_list(request):
    today = datetime.date.today()
    six_months_ago = today - datetime.timedelta(days=30 * 6)

    incomes = UserIncome.objects.filter(owner=request.user,
                                        date__gte=six_months_ago, date__lte=today)

    source_data = {}
    for income in incomes:
        source_name = income.source.name  # Corrected attribute access
        source_data[source_name] = source_data.get(source_name, 0) + income.amount

    return JsonResponse({'income_source_data': source_data})




@login_required(login_url='/authentication/login')
def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        incomes = UserIncome.objects.filter(
            Q(amount__istartswith=search_str) |
            Q(date__icontains=search_str) |
            Q(description__icontains=search_str) |
            Q(source__name__icontains=search_str),
            owner=request.user
        )
        data = [
            {
                'amount': income.amount,
                'source': income.source.name if income.source else "Uncategorized",
                'description': income.description,
                'date': income.date.strftime('%Y-%m-%d')  # Format date as needed
            }
            for income in incomes
        ]
        return JsonResponse(data, safe=False)




@login_required(login_url='/authentication/login')
def index(request):
    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Corrected method call
    try:
        # Attempt to retrieve UserPreferences for the current user
        user_preferences = UserPreferences.objects.get(user=request.user)
        currency = user_preferences.currency
    except UserPreferences.DoesNotExist:
        # Handle the case where UserPreferences does not exist
        currency = None  # Or provide a default currency
        
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST,
        }

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('income_date')
        source = request.POST.get('source')  # Get the source name from the form

        if not amount.isdigit():
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', context)

        if not source:
            messages.error(request, 'source is required')
            return render(request, 'income/add_income.html', context)

        try:
            # Get the source instance based on the name provided in the form
            source = Source.objects.get(name=source)
        except Source.DoesNotExist:
            messages.error(request, 'Invalid source')
            return render(request, 'income/add_income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, date=date, 
                               source=source, description=description)
        
        messages.success(request, 'record saved successfully')

        return redirect('income:index')  # Redirect to the index view of income app

    return render(request, 'income/add_income.html', context)

#edit
@login_required(login_url='/authentication/login')
def Edit_Income(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources':sources

    }

    if request.method == 'GET':
        return render(request, 'income/edit_data.html', context)
    
    elif request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('income_date')
        source = request.POST.get('source')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_data.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_data.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/edit_data.html', context)

        if not source:
            messages.error(request, 'source is required')
            return render(request, 'income/edit_data.html', context)

        try:
            source = Source.objects.get(name=source)
        except source.DoesNotExist:
            messages.error(request, 'Invalid source')
            return render(request, 'income/edit_data.html', context)

        # Update the income object with the new values
        income.owner = request.user
        income.amount = amount
        income.description = description
        income.date = date
        income.source = source
        income.save()

        messages.success(request, 'income updated successfully')

        return redirect('income:index')

#delete
@login_required(login_url='/authentication/login')
def delete_data(request, id):
    try:
        income = UserIncome.objects.get(pk=id)
        income.delete()
        messages.success(request, 'Record removed successfully')
    except UserIncome.DoesNotExist:
        messages.error(request, 'Income record not found')
    return redirect('income:index')