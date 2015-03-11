
# -*- encoding: utf-8 -*-
#core Django Imports
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.forms.extras import widgets

#Third party apps
#Project apps import
from .models import UserProfile, Category, Event, MailingList, Organization

class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Password',
         widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}))
    password2 = forms.CharField(label='Password confirmation',
        widget=forms.PasswordInput(attrs={'placeholder':'Confirmar Contraseña'}))
    username = forms.CharField(required=False, max_length=30)
    full_name = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={"placeholder":'Nombre Completo'}))
    email = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={"placeholder":'Email'}))

    class Meta:
        model = UserProfile
        fields = ('email', 'full_name')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # field does not have access to the initial value
        # This is done here, rather than on the field, because the
        return self.initial["password"]

    def clean_password2(self):
            # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
                        raise forms.ValidationError("Passwords don't match")
        return password2

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        #change the html class of all the elements
        for field in self.fields:
        #of the form to get bootstrap 3 styling
            self.fields[field].widget.attrs.update({'class':'form-control'})

        self.fields.keyOrder = ['email', 'full_name', 'password1', 'password2']
    def save(self, commit=True):
                # Save the provided password in hashed format
        user = super(CustomUserCreationForm, self).save(commit=False)
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
        fields = ('full_name', 'email')
        widgets = {'user_form': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(UserProfileChangeForm, self).__init__(*args, **kwargs)
        #change the html class of all the elements of the form to get bootstrap 3 styling
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})


class  UserProfileLoginForm(AuthenticationForm):
    """A Form for user login."""
    form_fields = ["username", "password"]
    username = forms.CharField(max_length=254, label="Correo Electronico",
        widget=forms.TextInput(attrs={"placeholder":'Usuario'}))
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

    def __init__(self, *args, **kwargs):
        super(UserProfileLoginForm, self).__init__(*args, **kwargs)
        #change the html class of all the elements of the form to get bootstrap 3 styling
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})


class OrganizationForm(forms.ModelForm):

    description = forms.CharField(label="Descripción", required=False,
                                  widget=forms.Textarea(attrs={'rows':'2'})
                                 )
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        """declaration of the inherited class"""
        model = Organization
        fields = ('name',
                  'description',
                  'phone',
                  'url',
                  'address',
                  'province',
                  'categories',
                 )

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        #change the html class of all the elements
        #of the form to get bootstrap 3 styling
        for field in self.fields:
            if field != 'categories':
                self.fields[field].widget.attrs.update({'class':'form-control'})
            else:
                self.fields[field].widget.attrs.update({'class':'organization-category'})


class OrganizationPictureForm(forms.ModelForm):
    picture = forms.ImageField()

    class Meta:
        model = Organization
        fields = (
                'logo',
                )


class EventForm(forms.ModelForm):
    """Form to handle event forms"""
    description = forms.CharField(label="Descripción", widget=forms.Textarea(attrs={'rows':'5'}))
    from_date = forms.CharField(widget=forms.TextInput(attrs={
            'class':'date',
            })
        )
    to_date = forms.CharField(widget=forms.TextInput(attrs={
            'class':'date',
            })
        )

    class Meta:
        """Model inheritance settings"""
        model = Event
        fields = ('name',
                  'categories',
                  'cost',
                  'description',
                  'from_date',
                  'to_date',
                  'url',
                 )


    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        #change the html class of all the elements of the form to get bootstrap 3 styling
        for field in self.fields:
            if field != 'categories':
                self.fields[field].widget.attrs.update({'class':'form-control'})
            else:
                self.fields[field].widget.attrs.update({'class':'event-category'})


class MailingListForm(forms.ModelForm):

    class Meta:
        Model = MailingList
        fields = (
                'full_name',
                'email',
                'province',
                )

