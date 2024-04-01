from django.contrib import admin
from .models import Expense, Category
# Register your models here.\


#display the admin table
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount','description','owner','category','date')
    search_fields = ('description', 'owner__username', 'category__name')

    list_per_page = 5
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)