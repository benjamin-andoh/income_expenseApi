import datetime
from rest_framework.views import APIView
from rest_framework import status, response
from _expenses.models import Expense
from _income.models import Income


class ExpenseSummaryStats(APIView):
    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(categories=category)
        amount = 0

        for expense in expenses:
            amount += expense.amount

        # convert decimal field into a str
        return {'amount': str(amount)}

    def get_category(self, expenses):
        return expenses.categories

    def get(self, request):
        today_date = datetime.date.today()
        a_year_ago = today_date - datetime.timedelta(days=30 * 12)
        expenses = Expense.objects.filter(owner=request.user,
                                          date__gte=a_year_ago,
                                          date__lte=today_date
                                          )
        final = {}

        # map though expenses and for each expenses get the category
        # set will remove all duplicate
        categories = list(set(map(self.get_category, expenses)))

        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(
                    expenses, category)
        return response.Response(
            {'category_data': final},
            status=status.HTTP_200_OK
        )


class IncomeSourceStats(APIView):
    def get_amount_for_source(self, income_list, source):
        income = income_list.filter(source=source)
        amount = 0

        for _i in income:
            amount += _i.amount

        # convert decimal field into a str
        return {'amount': str(amount)}

    def get_source(self, income):
        return income.source

    def get(self, request):
        today_date = datetime.date.today()
        a_year_ago = today_date - datetime.timedelta(days=30 * 12)
        income = Income.objects.filter(owner=request.user,
                                       date__gte=a_year_ago,
                                       date__lte=today_date
                                       )
        final = {}

        # map though expenses and for each expenses get the category
        # set will remove all duplicate
        sources = list(set(map(self.get_source, income)))

        for _i in income:
            for source in sources:
                final[source] = self.get_amount_for_source(
                    income, source)
        return response.Response(
            {'income_source_data': final},
            status=status.HTTP_200_OK
        )
