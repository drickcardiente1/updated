from enum import unique
from typing import Type
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django import forms

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control','id':'email', "style":"margin: 0;"}),required=True)
    otp = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"OTP", "class":"form-control", "type":"number", "id":"otp","oninput":"javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);", "maxlength":"7", "style":"margin: 0;"}),required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control','id':'username',"style":"margin: 0;"}),required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control','id':'first_name', "style":"margin: 0;"}),required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control','id':'last_name', "style":"margin: 0;"}),required=True)
    mobile = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Mobile Number (Optional)','class': 'form-control','id':'mobile', "style":"margin: 0;"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','id':'pwd', "style":"margin: 0;"}),required=True)
    receive_notif = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input',"type":"checkbox", 'id':'receive_notif'}))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control','id':'username',"style":"margin: 0;"}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','id':'pwd', "style":"margin: 0;"}),required=True)

class Password_Reset_Confirm(forms.Form):
    otp = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"OTP","onFocus":"clearotp()", "class":"form-control", "type":"number", "id":"otp","oninput":"javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);", "maxlength":"7", "style":"margin: 0; color: black;"}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','id':'nwpwd', "style":"margin: 0; color: black;","onFocus":"clearpwd()"}),required=True)
