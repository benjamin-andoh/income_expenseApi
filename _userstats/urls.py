from django.urls import path
from .views import ExpenseSummaryStats, IncomeSourceStats

urlpatterns = [
    path('expenses_category_data',
         ExpenseSummaryStats.as_view(),
         name='expenses_category_data'),

    path('income_source_data',
         IncomeSourceStats.as_view(),
         name='income_source_data')
]
