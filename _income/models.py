from django.db import models

from _config import settings

SOURCE = [
    ('SALARY', 'salary'),
    ('BUSINESS', 'business'),
    ('SIDE_HUSTLE', 'side_hustle'),
    ('OTHER', 'other'),
]


class Income(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='income'
    )
    source = models.CharField(
        choices=SOURCE,
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
