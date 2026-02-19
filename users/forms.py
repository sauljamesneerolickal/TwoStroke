from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.core.validators import RegexValidator

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        max_length=10, 
        min_length=10,
        required=True,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.')],
        widget=forms.TextInput(attrs={'placeholder': '10-digit mobile number'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        user.is_approved = True
        if commit:
            user.save()
        return user

class SellerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        max_length=10, 
        min_length=10,
        required=True,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.')],
        widget=forms.TextInput(attrs={'placeholder': '10-digit mobile number'})
    )
    workshop_name = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'workshop_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'seller'
        user.is_approved = False
        if commit:
            user.save()
        return user

class AdminUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        max_length=10, 
        min_length=10,
        required=True,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number.')],
        widget=forms.TextInput(attrs={'placeholder': '10-digit mobile number'})
    )
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    workshop_name = forms.CharField(max_length=100, required=False, help_text="Required if role is Seller.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'role', 'workshop_name')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if user.role == 'customer':
            user.is_approved = True
        elif user.role == 'seller':
            user.is_approved = True # Admin created sellers are auto-approved? Or maybe not. Let's say yes for convenience.
            user.workshop_name = self.cleaned_data.get('workshop_name')
        elif user.role == 'admin':
            user.is_approved = True
            user.is_staff = True
            user.is_superuser = True
        
        if commit:
            user.save()
        return user

class SpareTrackLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_picture', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'profile_picture':
                self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': field.replace('_', ' ').capitalize()})
