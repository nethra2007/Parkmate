from django.shortcuts import render, redirect, get_object_or_404
from .models import ParkingSlot
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import AuthenticationForm
@staff_member_required
def add_slot(request):
    if request.method == 'POST':
        slot_number = request.POST.get('slot_number')
        if not ParkingSlot.objects.filter(slot_number=slot_number).exists():
            ParkingSlot.objects.create(slot_number=slot_number)
        return redirect('home')
    return render(request, 'add_slot.html')

@staff_member_required
def delete_slot(request, slot_id):
    slot = get_object_or_404(ParkingSlot, slot_number=slot_id)
    slot.delete()
    return redirect('home')

@login_required
def home(request):
    slots = ParkingSlot.objects.all().order_by('slot_number')

    search_query = request.GET.get('search', '').strip()
    filter_status = request.GET.get('filter', '')

    # Safe chaining of queries
    if search_query:
        import re
        try:
            regex_pattern = re.compile(f".*{re.escape(search_query)}.*", re.IGNORECASE)
            slots = slots.filter(slot_number__regex=regex_pattern)
        except Exception as e:
            print("Regex error:", e)

    if filter_status == 'available':
        slots = slots.filter(is_occupied=False)
    elif filter_status == 'occupied':
        slots = slots.filter(is_occupied=True)

    return render(request, 'home.html', {'slots': slots})

@login_required
def reserve_slot(request, slot_id):
    slot = get_object_or_404(ParkingSlot, slot_number=slot_id)

    if request.method == "POST":
        client_name = request.POST.get("client_name")
        vehicle_number = request.POST.get("vehicle_number")
        slot.client_name = client_name
        slot.vehicle_number = vehicle_number
        slot.is_occupied = True
        slot.booked_by = request.user  
        slot.save()
        return redirect('home')

    return render(request, 'reserve_form.html', {'slot': slot})

from django.http import HttpResponseForbidden

@login_required
def cancel_slot(request, slot_id):
    slot = get_object_or_404(ParkingSlot, slot_number=slot_id)
    # Only the user who booked it OR an admin can cancel
    if slot.booked_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to cancel this booking.")
    slot.is_occupied = False
    slot.client_name = ""
    slot.vehicle_number = ""
    slot.booked_by = None
    slot.save()
    return redirect('home')

@login_required
def my_bookings(request):
    if request.user.is_superuser:
        return redirect('home')  
    slots = ParkingSlot.objects.filter(booked_by=request.user)
    return render(request, 'my_bookings.html', {'slots': slots})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False          #  Not an admin
            user.is_superuser = False      #  Not a superuser
            user.is_active = True          #  Allow login
            user.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  # Debug if needed
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})
def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # or your dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})