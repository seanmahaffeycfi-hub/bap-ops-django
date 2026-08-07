from django.db import models
from bap_ops_django.choices import RECORD_TYPE_CHOICES


class MileageEntry(models.Model):
    date = models.DateField()
    start_mileage = models.DecimalField(max_digits=10, decimal_places=1)
    end_mileage = models.DecimalField(max_digits=10, decimal_places=1)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES)
    start_lat = models.FloatField(blank=True, null=True)
    start_lng = models.FloatField(blank=True, null=True)
    end_lat = models.FloatField(blank=True, null=True)
    end_lng = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    @property
    def miles_driven(self):
        return self.end_mileage - self.start_mileage

    def __str__(self):
        return f"{self.date} — {self.miles_driven} mi ({self.get_record_type_display()})"