from django.db import models


class Donation(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    donor_name = models.CharField(max_length=255)
    receipt_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} — {self.donor_name} (${self.value})"