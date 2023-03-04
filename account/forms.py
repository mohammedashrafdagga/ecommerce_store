from django import forms
from .models import UserBase
from django.contrib.auth.forms import AuthenticationForm


class RegisterUserForm(forms.ModelForm):
    
    username = forms.CharField(label='username', max_length=50, help_text='Required')
    email  = forms.EmailField(label = 'email', help_text='Required', max_length=100, error_messages={'required': 'Sorry, this fields is required'})
    
    password1 = forms.CharField(label='password',  widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    
    
    class Meta:
        model = UserBase
        fields = ('email', 'username', )    
        
        
    # Clean up for field
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        user = UserBase.objects.filter(username = username).exists()
        if user:
            raise forms.ValidationError('Username Already Exists, Use another')
        # this is if not exists
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = UserBase.objects.filter(email = email).exists()
        if user:
            raise forms.ValidationError('email Already Exists, Use another')
        # this is if not exists
        return email 
    
    # validation password
    def clean_password2(self):
        # if not matches
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('password and confirm password is not match')
        #  if matches
        return self.cleaned_data['password2']
    
    
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='username', max_length=50, help_text='Required')
    password = forms.CharField(label='password',  widget=forms.PasswordInput)