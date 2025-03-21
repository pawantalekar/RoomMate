from django.urls import path
from .views import (
    login_register_view, home_view, profile_view, edit_profile_view, logout_view,
    room_list_view, room_detail_view, add_room_view, edit_room_view, delete_room_view, my_rooms,
    admin_login, admin_dashboard  # Import admin views directly
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name='home'),  # Root URL (/) for home page
    path('home/', home_view, name='home'),  # Explicit /home/ for consistency
    path('login/', login_register_view, name='login_register'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('logout/', logout_view, name='logout'),
    path('rooms/', room_list_view, name='room_list'),
    path('rooms/<int:room_id>/', room_detail_view, name='room_detail'),
    path('rooms/add/', add_room_view, name='add_room'),
    path('rooms/edit/<int:room_id>/', edit_room_view, name='edit_room'),
    path('rooms/delete/<int:room_id>/', delete_room_view, name='delete_room'),
    path('rooms/delete/', delete_room_view, name='delete_room_all'),  # Kept as is, assuming it’s intentional
    path('my-rooms/', my_rooms, name='my_rooms'),
    path('admin-login/', admin_login, name='admin_login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)