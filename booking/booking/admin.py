from django.contrib import admin
from .models import Feature, Room, Booking
from django.db import models
from django.forms import Textarea

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'capacity', 'price', 'is_active')
    list_filter = ('room_type', 'is_active', 'features')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'price')
    filter_horizontal = ('features',)

    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'start_time', 'room__room_type')
    search_fields = ('room__name', 'user__username', 'user__email')
    list_editable = ('status',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    actions = ['approve_bookings', 'cancel_bookings']

    @admin.action(description='Підтвердити обрані бронювання')
    def approve_bookings(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f"Обрані бронювання успішно підтверджені.")

    @admin.action(description='Скасувати обрані бронювання')
    def cancel_bookings(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"Обрані бронювання успішно скасовані.")