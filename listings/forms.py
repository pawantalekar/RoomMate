# listings/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Facility, Profile, RoomListing, RoomImage

# Custom widget and field for multiple file uploads (unchanged)
class CustomMultiFileInput(forms.Widget):
    template_name = 'django/forms/widgets/file.html'
    input_type = 'file'

    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
        else:
            attrs = {}
        attrs['multiple'] = True
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context

    def value_from_datadict(self, data, files, name):
        if name in files:
            return files.getlist(name)
        return None

class MultipleFileField(forms.FileField):
    widget = CustomMultiFileInput

    def clean(self, data, initial=None):
        if not data:
            return []
        return data

class RoomForm(forms.ModelForm):
    facilities = forms.ModelMultipleChoiceField(
        queryset=Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'facility-checkbox'}),
        required=False
    )
    additional_images = MultipleFileField(
        required=False,
        label='Additional Images'
    )
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = RoomListing
        fields = [
            'title', 'description', 'price', 'location', 'latitude', 'longitude',
            'room_type', 'for_whom', 'facilities', 'main_image', 'contact_number'
        ]
        widgets = {
            'main_image': forms.ClearableFileInput(),
        }

    def save(self, commit=True, user=None):
        room = super().save(commit=False)
        if user:
            room.user = user
        if commit:
            room.save()
            self.save_m2m()
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
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Who are you?'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Create Profile with role
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )
        return user

class LoginForm(AuthenticationForm):
    pass