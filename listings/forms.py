from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Facility, Profile, RoomListing, RoomImage

class RoomForm(forms.ModelForm):
    facilities = forms.ModelMultipleChoiceField(
        queryset=Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'facility-checkbox'}),
        required=False
    )
    additional_images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = RoomListing
        fields = [
            'title', 'description', 'price', 'location', 'latitude', 'longitude',
            'room_type', 'for_whom', 'facilities', 'main_image', 'contact_number'
        ]

    def save(self, commit=True, user=None):
        room = super().save(commit=False)
        if user:
            room.user = user
        if commit:
            room.save()
            self.save_m2m()  # Save ManyToMany fields (facilities)
            additional_images = self.files.getlist('additional_images')
            for image in additional_images:
                RoomImage.objects.create(room=room, image=image)
        return room

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'profile_picture']

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        
        return cleaned_data

class LoginForm(AuthenticationForm):
    pass