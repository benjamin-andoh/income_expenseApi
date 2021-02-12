from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from _expenses.models import Expense
from _expenses.permissions import IsOwner
from _expenses.serializers import ExpenseSerializer
from rest_framework import permissions


class ExpenseListAPIVIew(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects
    model = Expense
    permission_classes = permissions.IsAuthenticated, IsOwner,

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailAPIVIew(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects
    permission_classes = permissions.IsAuthenticated, IsOwner,
    lookup_field = 'pk'

    # def get_queryset(self):
    #     obj = self.queryset.filter(owner=self.request.user)
    #     return obj
