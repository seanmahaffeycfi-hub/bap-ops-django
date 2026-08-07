from django.db import models
from bap_ops_django.choices import RECORD_TYPE_CHOICES


class Expense(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    is_car_expense = models.BooleanField(default=False)
    receipt_image_url = models.URLField(blank=True, null=True)
    ocr_raw_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} — {self.description} (${self.amount})"