from django.urls import path

from _expenses.views import ExpenseListAPIVIew, ExpenseDetailAPIVIew

urlpatterns = [
    path('list', ExpenseListAPIVIew.as_view(), name='expense-list'),
    path('create', ExpenseListAPIVIew.as_view(), name='expense-create'),
    path('detail/<pk>', ExpenseDetailAPIVIew.as_view(), name='expense-detail'),
    path('update/<pk>', ExpenseDetailAPIVIew.as_view(), name='expense-update'),
    path('delete/<pk>', ExpenseDetailAPIVIew.as_view(), name='expense-delete')

]
