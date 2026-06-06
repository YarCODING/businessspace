from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Feature(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва зручності")

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ('desk', 'Робоче місце'),
        ('meeting', 'Переговорна кімната'),
        ('conference', 'Конференц-зал'),
    ]

    name = models.CharField(max_length=150, verbose_name="Назва/Номер")
    description = models.CharField(max_length=480, verbose_name="Опис", default='Опису не додано')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, verbose_name="Тип")
    capacity = models.PositiveIntegerField(verbose_name="Вмістимість (чол.)")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    features = models.ManyToManyField(Feature, blank=True, verbose_name="Особливості")
    is_active = models.BooleanField(default=True, verbose_name="Доступна для бронювання")

    def __str__(self):
        return f"{self.get_room_type_display()} - {self.name}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує підтвердження'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Кімната/Місце")
    start_time = models.DateField(verbose_name="Дата початку")
    end_time = models.DateField(verbose_name="Дата завершення")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Бронювання #{self.id} - {self.room.name} ({self.user.username})"

    def clean(self):
        if not hasattr(self, 'room') or self.room is None:
            return
        
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("Час початку не може бути більшим або рівним часу завершення.")
            
            overlapping_bookings = Booking.objects.filter(
                room=self.room,
                status='confirmed',
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk)
            
            if overlapping_bookings.exists():
                raise ValidationError("Цей період часу для обраної кімнати вже заброньовано.")