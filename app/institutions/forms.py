#core Django Imports
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm

#Third party apps
from captcha.fields import CaptchaField

#Project apps import
from .models import UserProfile

class UserProfileCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    form_fields = [
                'password1',
                'password2',
                'email',
                'name',
                'description',
                'logo',
                'phone',
                'is_phone_visible',
                'address',
                'is_address_visible',
               ]

    password1 = forms.CharField(label='Password',
         widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
        widget=forms.PasswordInput)
    captcha = CaptchaField()

    class Meta:
        model = UserProfile
        fields = ('email',
                  'name',
                  'description',
                  'logo',
                  'phone',
                  'is_phone_visible',
                  'address',
                  'is_address_visible',
                )

    def clean_password2(self):
            # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
                        raise forms.ValidationError("Passwords don't match")
        return password2

    def __init__(self, *args, **kwargs):
        super(UserProfileCreationForm, self).__init__(*args, **kwargs)
        #change the html class of all the elements of the form to get bootstrap 3 styling
        for field in self.form_fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})

    def save(self, commit=True):
                # Save the provided password in hashed format
        user = super(UserProfileCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class  UserProfileLoginForm(AuthenticationForm):
    """A Form for user login."""
    form_fields = ["username", "password"]

    username = forms.CharField(max_length=254, label="Correo Electronico")

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        #change the html class of all the elements of the form to get bootstrap 3 styling
        for field in self.form_fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})
