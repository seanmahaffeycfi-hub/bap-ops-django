from django.db import models


class VaseReceived(models.Model):
    date_received = models.DateField()
    quantity = models.PositiveIntegerField()
    poc_name = models.CharField(max_length=255)
    poc_facility_name = models.CharField(max_length=255, blank=True)
    poc_phone = models.CharField(max_length=30, blank=True)
    poc_email = models.EmailField(blank=True)
    recipient = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_received']

    def __str__(self):
        return f"{self.date_received} — {self.quantity} vases to {self.recipient}"


class VaseReturned(models.Model):
    date_returned = models.DateField()
    quantity = models.PositiveIntegerField()
    returned_from = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_returned']

    def __str__(self):
        return f"{self.date_returned} — {self.quantity} vases from {self.returned_from}"


class VaseReceived(models.Model):
    date_received = models.DateField()
    quantity = models.PositiveIntegerField()
    poc_name = models.CharField(max_length=255)
    poc_facility_name = models.CharField(max_length=255, blank=True)
    poc_phone = models.CharField(max_length=30, blank=True)
    poc_email = models.EmailField(blank=True)
    recipient = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_received']

    def __str__(self):
        return f"{self.date_received} — {self.quantity} vases to {self.recipient}"


class VaseReturned(models.Model):
    date_returned = models.DateField()
    quantity = models.PositiveIntegerField()
    returned_from = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_returned']

    def __str__(self):
        return f"{self.date_returned} — {self.quantity} vases from {self.returned_from}"