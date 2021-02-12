from rest_framework import serializers

from _expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'owner', 'categories', 'amount', 'description', 'date']

        extra_kwargs = {
            'date': {'read_only': True},
            'owner': {'read_only': True},
        }
