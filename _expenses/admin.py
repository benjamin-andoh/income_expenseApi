from django.contrib import admin
from _expenses.models import Expense


class BlogExpenseAdmin(admin.ModelAdmin):
    model = Expense
    list_display = [
       'id', 'owner', 'categories', 'amount', 'description', 'date'
    ]


admin.site.register(Expense, BlogExpenseAdmin)
