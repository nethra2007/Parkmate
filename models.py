from django.db import models
from django.contrib.auth.models import User
class ParkingSlot(models.Model):
    slot_number = models.CharField(max_length=10, unique=True)
    is_occupied = models.BooleanField(default=False)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    vehicle_number = models.CharField(max_length=15, blank=True, null=True)
    reserved_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"Slot {self.slot_number} - {'Occupied' if self.is_occupied else 'Available'}"
