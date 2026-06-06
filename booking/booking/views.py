import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Room, Booking, Feature
from .forms import BookingForm

def index(request):
    featured_rooms = Room.objects.filter(is_active=True).order_by('-id')[:3]
    return render(request, 'booking/index.html', {'rooms': featured_rooms})

def room_list(request):
    rooms = Room.objects.filter(is_active=True)

    room_type = request.GET.get('type')
    if room_type:
        rooms = rooms.filter(room_type=room_type)

    feature_id = request.GET.get('feature')
    if feature_id:
        rooms = rooms.filter(features__id=feature_id)

    room_types = Room.ROOM_TYPES
    features = Feature.objects.all()

    return render(request, 'booking/room_list.html', {
        'rooms': rooms,
        'room_types': room_types,
        'features': features
    })

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    existing_bookings = Booking.objects.filter(room=room, status='confirmed')

    booked_ranges = []
    for booking in existing_bookings:
        booked_ranges.append({
            'from': booking.start_time.strftime('%Y-%m-%d'),
            'to': booking.end_time.strftime('%Y-%m-%d')
        })
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                
                booking.user = request.user
                booking.room = room
                
                try:
                    booking.full_clean()
                    booking.save()
                    return redirect('user_bookings')
                except ValidationError as e:
                    form.add_error(None, e)
        else:
            return redirect('login') 
    else:
        form = BookingForm()
        
    return render(request, 'booking/room_detail.html', {
        'room': room,
        'form': form,
        'booked_ranges': json.dumps(booked_ranges)
    })

@login_required(login_url='/accounts/login/')
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/user_bookings.html', {'bookings': bookings})