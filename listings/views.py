from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, RoomListing, RoomImage, Facility
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, RoomForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import RoomListing, Facility
from django.contrib.auth.models import User
from math import radians, sin, cos, sqrt, atan2



def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers using Haversine formula."""
    R = 6371  # Earth's radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# ===============================
# LOGIN & REGISTER VIEW
# ===============================
def login_register_view(request):
    reg_form = RegistrationForm(request.POST or None)
    login_form = LoginForm(request, data=request.POST or None)
    login_error = None
    reg_error = None

    if request.method == 'POST':
        if 'register' in request.POST:
            if reg_form.is_valid():
                user = reg_form.save(commit=False)
                user.set_password(reg_form.cleaned_data['password'])
                user.save()
                login(request, user)
                return redirect('home')
            else:
                reg_error = "Please correct the errors below."

        elif 'login' in request.POST:
            if login_form.is_valid():
                user = authenticate(
                    request,
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    login_error = "Invalid username or password. Please try again."
            else:
                login_error = "Please correct the errors below."

    return render(request, 'listings/login_register.html', {
        'reg_form': reg_form,
        'login_form': login_form,
        'login_error': login_error,
        'reg_error': reg_error,
    })

# ===============================
# PROFILE VIEWS
# ===============================
@login_required
def profile_view(request):
    return render(request, 'listings/profile.html')

@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'listings/edit_profile.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_register')

# ===============================
# ROOM LISTING VIEWS
# ===============================



def home_view(request):
    rooms = RoomListing.objects.all()
    all_facilities = Facility.objects.all()
    selected_facilities = request.GET.getlist('facilities')
    room_type = request.GET.get('room_type', '')
    for_whom = request.GET.get('for_whom', '')
    location_query = request.GET.get('location', '')
    max_price = request.GET.get('max_price', '')

    # Filter by room type
    if room_type:
        rooms = rooms.filter(room_type=room_type)

    # Filter by for_whom
    if for_whom:
        rooms = rooms.filter(for_whom=for_whom)

    # Filter by facilities
    if selected_facilities:
        for facility in selected_facilities:
            rooms = rooms.filter(facilities__name=facility)

    # Filter by max price
    if max_price:
        rooms = rooms.filter(price__lte=float(max_price))

    # Filter by location (coordinates or text)
    if location_query:
        try:
            # Check if location_query is in "lat, lon" format
            lat_str, lon_str = location_query.split(',')
            search_lat = float(lat_str.strip())
            search_lon = float(lon_str.strip())

            # Filter rooms within 10km radius
            filtered_rooms = []
            for room in rooms:
                if room.latitude and room.longitude:
                    distance = haversine(search_lat, search_lon, room.latitude, room.longitude)
                    if distance <= 10:  # 10km radius
                        filtered_rooms.append(room.id)
            rooms = rooms.filter(id__in=filtered_rooms)
        except (ValueError, IndexError):
            # If not coordinates, filter by text location
            rooms = rooms.filter(location__icontains=location_query)

    context = {
        'rooms': rooms,
        'all_facilities': all_facilities,
        'selected_facilities': selected_facilities,
        'room_type_choices': RoomListing.ROOM_TYPE_CHOICES,  # Adjust based on your model
        'for_whom_choices': RoomListing.FOR_WHOM_CHOICES,    # Adjust based on your model
    }
    return render(request, 'listings/home.html', context)



@login_required
def room_list_view(request):
    rooms = RoomListing.objects.filter(available=True).order_by('-created_at')
    location = request.GET.get('location', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    if location:
        rooms = rooms.filter(location__icontains=location)
    
    try:
        if min_price:
            rooms = rooms.filter(price__gte=int(min_price))
        if max_price:
            rooms = rooms.filter(price__lte=int(max_price))
    except ValueError:
        pass

    return render(request, 'listings/room_list.html', {'rooms': rooms})

@login_required
def room_detail_view(request, room_id):
    room = get_object_or_404(RoomListing, id=room_id)
    return render(request, 'listings/room_detail.html', {'room': room})

@login_required
def add_room_view(request):
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(user=request.user)  # Pass user to custom save method
            return redirect('room_detail', room_id=room.id)
        else:
            print(form.errors)  # Debug form errors in console
    else:
        form = RoomForm()
    
    return render(request, 'listings/add_room.html', {'form': form})

@login_required
def edit_room_view(request, room_id):
    room = get_object_or_404(RoomListing, id=room_id, user=request.user)
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            room = form.save()  # No user needed for edit, instance already has it
            return redirect('room_detail', room_id=room.id)
        else:
            print(form.errors)  # Debug form errors in console
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'listings/edit_room.html', {
        'room': room,
        'form': form,
        'all_facilities': Facility.objects.all(),
        'selected_facilities': room.facilities.values_list('id', flat=True)
    })

@login_required
def my_rooms(request):
    rooms = RoomListing.objects.filter(user=request.user)
    return render(request, 'listings/my_rooms.html', {'rooms': rooms})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import RoomListing, Facility
from django.contrib.auth.hashers import make_password

@login_required
def delete_room_view(request, room_id=None):
    if room_id:
        if request.user.is_superuser:
            room = get_object_or_404(RoomListing, id=room_id)
            if request.method == "POST":
                room.delete()
                return redirect('admin_dashboard')
            return render(request, 'listings/delete_room.html', {'room': room})
        else:
            room = get_object_or_404(RoomListing, id=room_id, user=request.user)
            if request.method == "POST":
                room.delete()
                return redirect('my_rooms')
            return render(request, 'listings/delete_room.html', {'room': room})
    if not request.user.is_superuser:
        rooms = RoomListing.objects.filter(user=request.user)
        return render(request, 'listings/delete_room.html', {'rooms': rooms})
    return redirect('admin_dashboard')

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not an admin.")
            return redirect('admin_login')
    return render(request, 'listings/admin_login.html')

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    section = request.GET.get('section', 'overview')

    if request.method == "POST":
        action = request.POST.get('action')
        
        # Add User
        if action == 'add_user':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                User.objects.create(username=username, email=email, password=make_password(password))
                messages.success(request, "User added successfully.")
        
        # Delete User
        elif action == 'delete_user':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            if user != request.user:  # Prevent self-deletion
                user.delete()
                messages.success(request, "User deleted successfully.")
            else:
                messages.error(request, "You cannot delete yourself.")
        
        # Add Facility
        elif action == 'add_facility':
            name = request.POST.get('name')
            if Facility.objects.filter(name=name).exists():
                messages.error(request, "Facility already exists.")
            else:
                Facility.objects.create(name=name)
                messages.success(request, "Facility added successfully.")
        
        # Delete Facility
        elif action == 'delete_facility':
            facility_id = request.POST.get('facility_id')
            facility = get_object_or_404(Facility, id=facility_id)
            facility.delete()
            messages.success(request, "Facility deleted successfully.")
        
        return redirect(f'/admin-dashboard/?section={section}')

    context = {
        'total_users': User.objects.count(),
        'total_rooms': RoomListing.objects.count(),
        'total_facilities': Facility.objects.count(),
        'recent_rooms': RoomListing.objects.order_by('-created_at')[:5],
        'users': User.objects.all(),
        'rooms': RoomListing.objects.all(),
        'facilities': Facility.objects.all(),
        'current_section': section,
        'messages': messages.get_messages(request),
    }
    return render(request, 'listings/admin_dashboard.html', context)

