from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate
from .models import CustomUser, Profile


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update(
            {
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }
        )
        self.fields['new_password2'].widget.attrs.update(
            {
                'class': 'form-control',
                'style': 'max-width: 300px',
            }
        )


class LoginForm(AuthenticationForm):  # AuthenticationForm for updating it for LoginView
    # username = None  # to remove the requirement for the "username" field.

    username = forms.CharField(  # expects both email and username
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Username/Email',
            }
        )
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px',
                'placeholder': 'Password'
            }
        )
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct email/username and password."
        ),
        'inactive': (
            "This account is inactive."
        ),
    }

    def clear(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        print(form.errors)
        return self.cleaned_data


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # first_name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # last_name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'

        for fieldname in ['username', 'email']:  # to remove help_text
            self.fields[fieldname].help_text = None

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if CustomUser.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize widget attributes for old_password field
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'style': 'max-width: 300px;',
            'placeholder': 'Old Password',
        })

        # Customize widget attributes for new_password1 field
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'style': 'max-width: 300px;',
            'placeholder': 'New Password',
        })

        # Customize widget attributes for new_password2 field
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'style': 'max-width: 300px;',
            'placeholder': 'Confirm New Password',
        })
    # old_password = forms.CharField(
    #     strip=False,
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'form-control',
    #             'style': 'max-width: 300px',
    #             'placeholder': 'Old Password'
    #         }
    #     )
    # )
    # new_password1 = forms.CharField(
    #     strip=False,
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'form-control',
    #             'style': 'max-width: 300px',
    #             'placeholder': 'New Password'
    #         }
    #     )
    # )
    # new_password2 = forms.CharField(
    #     strip=False,
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'form-control',
    #             'style': 'max-width: 300px',
    #             'placeholder': 'Repeat New Password'
    #         }
    #     )
    # )
    #
    # def __init__(self, *args, **kwargs):
    #     super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['old_password'].widget.attrs['class'] = 'form-control'


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)

        # Customize form fields here if needed
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'

        for fieldname in ['username', 'email']:  # to remove help_text
            self.fields[fieldname].help_text = None

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = CustomUser.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'id': 'image_field',
                'style': 'height: 40px; width: 110px;'
            }
        )
    )

    class Meta:
        model = Profile
        fields = ['photo']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        self.fields['photo'].widget.attrs['class'] = 'form-control'

