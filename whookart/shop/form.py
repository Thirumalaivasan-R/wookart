
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User
from django import forms

 
class CustomUserForm(UserCreationForm):
  username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
  email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}))
  password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
  password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password'}))
  class Meta:
    model=User
    fields=['username','email','password1','password2']
    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
    
class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email and self.instance:
            return self.instance.email  # Retain existing email if not entered
        return email

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
