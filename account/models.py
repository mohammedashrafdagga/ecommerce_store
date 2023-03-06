from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django_countries.fields import CountryField
# for translation
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.mail import send_mail



# Building Custom Account Manger 
class CustomAccountManger(BaseUserManager):
    
    # create super user customize again
    def create_superuser(self, email, username, password, **other_fields):
        # set  
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff = True'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser = True'
            )
            
        return self.create_user(email, username, password, **other_fields)
        

    
    def create_user(self, email, username, password, **other_fields):
        
        if not email:
            raise ValueError(_('you must provide a email address'))
    
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **other_fields)
        
        user.set_password(password)
        user.save()
        return user

class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name= models.CharField(max_length=150, blank=True)
    bio = models.TextField(_('bio'),  max_length=500,blank=True)
    
    # Delivery Info
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line1 = models.CharField(max_length=150, blank=True)
    address_line2 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    
    # user status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # Objects Manger
    objects = CustomAccountManger()
    
    # Username Filed and Email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    
    # Mete data
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
    
    # email user
    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )
        
        
    # what the return
    def __str__(self) -> str:
        return self.username
    