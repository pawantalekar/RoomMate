from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Profile Model for storing user information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Enter a valid phone number (e.g., +911234567890).",
            )
        ],
    )
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        default='profile_pics/default_profile.jpg'  # Optional default image
    )

    def __str__(self):
        return self.user.username


# Facility Model for managing facilities as checkboxes
class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Facilities"  # Correct plural form in admin


# Room Listing Model with filters
class RoomListing(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single_room', 'Single Room'),
        ('double_room', 'Double Room'),
        ('pg', 'PG'),
        ('hostel', 'Hostel'),
        ('guest_house', 'Guest House'),
        ('flat', 'Flat'),
    ]

    FOR_WHOM_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('all', 'All'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_listings')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200, blank=True, null=True)  # Increased max_length
    main_image = models.ImageField(
        upload_to='room_pics/',
        blank=True,
        null=True,
        default='room_pics/default_room.jpg'  # Optional default image
    )
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPE_CHOICES,
        blank=True,
        null=True
    )
    for_whom = models.CharField(
        max_length=20,
        choices=FOR_WHOM_CHOICES,
        blank=True,
        null=True
    )
    facilities = models.ManyToManyField(Facility, blank=True, related_name='rooms')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    contact_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Enter a valid phone number (e.g., +911234567890).",
            )
        ],
        help_text="Enter your contact number (e.g., +911234567890) for users to reach you."
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Default ordering by newest first


# Room Image Model to store additional room images
class RoomImage(models.Model):
    room = models.ForeignKey(
        RoomListing,
        related_name="additional_images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="room_pics/")

    def __str__(self):
        return f"Image for {self.room.title}"