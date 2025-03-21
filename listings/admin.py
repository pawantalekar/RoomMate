# listings/admin.py
from django.contrib import admin
from .models import Profile, Facility, RoomListing, RoomImage

@admin.register(RoomListing)
class RoomListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'contact_number', 'available')
    list_filter = ('room_type', 'for_whom', 'available')
    search_fields = ('title', 'location')

admin.site.register(Profile)
admin.site.register(Facility)
admin.site.register(RoomImage)