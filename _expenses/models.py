from django.db import models

from _config import settings


CATEGORIES = [
    ('ONLINE_SERVICE', 'online_service'),
    ('TRAVEL', 'travel'),
    ('FOOD', 'food'),
    ('RENT', 'rent'),
    ('OTHER', 'other'),
]


class Expense(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    categories = models.CharField(
        choices=CATEGORIES,
        max_length=200
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    date = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.owner) + 's income'
