from django.db import models
from guest.models import Guest
from room.models import Room
from django.urls import reverse


class Reservation(models.Model):
    room = models.ForeignKey('room.Room', on_delete=models.CASCADE)
    guest = models.ForeignKey('guest.Guest', on_delete=models.CASCADE)
    additional = models.TextField(null=True, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    
    def get_absolute_url(self):
        return reverse('reservation_detail', args=[str(self.id)])
    
    def __str__(self):
        return f"{self.room.room_number} | from {self.check_in_date} to {self.check_out_date}"

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'