from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from _expenses.permissions import IsOwner
from _expenses.serializers import ExpenseSerializer
from rest_framework import permissions
from _income.models import Income
from _income.serializers import IncomeSerializer


class IncomeListAPIVIew(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects
    model = Income
    permission_classes = permissions.IsAuthenticated, IsOwner,

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeDetailAPIVIew(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects
    permission_classes = permissions.IsAuthenticated, IsOwner,
    lookup_field = 'pk'

    def get_queryset(self):
        obj = self.queryset.filter(owner=self.request.user)
        return obj
