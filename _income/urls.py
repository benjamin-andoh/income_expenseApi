from django.urls import path

from _income.views import IncomeListAPIVIew, IncomeDetailAPIVIew

urlpatterns = [
    path('list', IncomeListAPIVIew.as_view(), name='expense-list'),
    path('create', IncomeListAPIVIew.as_view(), name='expense-create'),
    path('detail/<pk>', IncomeDetailAPIVIew.as_view(), name='expense-detail'),
    path('update/<pk>', IncomeDetailAPIVIew.as_view(), name='expense-update'),
    path('delete/<pk>', IncomeDetailAPIVIew.as_view(), name='expense-delete')

]
