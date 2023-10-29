from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class LoginUserForm(forms.ModelForm):
    username = forms.CharField(
        label = 'Username',
        required = True,
        max_length = 25,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id': 'username-input',
                'placeholder': 'Enter username',
                'aria-describedby': 'emailHelp',
            }
        )
    )

    password = forms.CharField(
        label = 'Password',
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'id': 'password-input',
                'placholder': 'Enter your password',
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )

    def clean(self, *args, **kwargs):
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('Invalid login')

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label = 'Username',
        required = True,
        max_length = 12,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id': 'username-input',
                'placeholder': 'Enter username',
            }
        )
    )

    email = forms.EmailField(
        label = 'Email address',
        max_length = 60,
        required = True,
        help_text = 'Required, but never shown',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id': 'email-input',
                'placeholder': 'name@example.com',
            }
        )
    )

    password1 = forms.CharField(
        required = True,
        label = 'Password',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'id': 'password-input',
                'placeholder': 'Enter password',
            }
        )
    )

    password2 = forms.CharField(
        required = True,
        label = 'Confirm password',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'id': 'password-confirm-input',
                'placeholder': 'Enter your password',
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

class MyProfileForm(UserChangeForm):
    username = forms.CharField(
        required = True,
        label = 'Username',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Your username...',
            }
        )
    )

    email = forms.EmailField(
        required = True,
        label = 'Emial address',
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Your email...',
            }
        )
    )

    image_url = forms.URLField(
        required = False,
        label = 'Avatar url',
        widget = forms.URLInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    facebook = forms.URLField(
        required = False,
        label = 'Facebook',
        widget = forms.URLInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    website = forms.URLField(
        required = False,
        label = 'Website',
        widget = forms.URLInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    description = forms.CharField(
        required = False,
        label = 'Description',
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'rows': 5,
            }
        )
    )


    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'image_url',
            'facebook',
            'website',
            'description',
        )