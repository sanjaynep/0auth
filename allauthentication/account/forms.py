import re
from django import forms
from account.models import User
from django.core.exceptions import ValidationError
import re

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    
    class Meta:
        model = User
        fields = ['full_name', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }

    #validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password:
            # Check if passwords match
            if password != confirm_password:
                raise forms.ValidationError("Password and Confirm Password do not match")

            # Check password length
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long")

            # Check for at least one letter and one digit
            if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
                raise forms.ValidationError("Password must contain both letters and numbers")

            # Check for at least one special character
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                raise forms.ValidationError("Password must include at least one special character")

        return cleaned_data

        
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
        

class passwordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),max_length=254,required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email does not exist")
        return email