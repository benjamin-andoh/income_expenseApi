from rest_framework import serializers
from _income.models import Income


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'owner', 'source', 'amount', 'description', 'date']

        extra_kwargs = {
            'date': {'read_only': True},
            'owner': {'read_only': True},
        }
