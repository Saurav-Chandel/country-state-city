from django.db import models
from django.utils import timezone
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin ,BaseUserManager



class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, password, **other_fields)

    def create_user(self, email, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)  
        user = self.model(email=email,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email addr'), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=254, blank=True, null=True)
    otp = models.CharField(max_length=250, null=True, blank=True)
    # phone = models.IntegerField(max_length=12,unique=True,blank=True,null=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
 
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email

    @staticmethod
    def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except:
            return False    


    def isExists(self):
        if User.objects.filter(email = self.email):
            return True

        return  False    




class Country(models.Model):
    country_code=models.CharField(max_length=50,null=True)
    name=models.CharField(max_length=100,verbose_name="Select Country")
    phonecode=models.IntegerField(max_length=100,null=True)

    def __str__(self):
        return self.name

class State1(models.Model):
    state_id=models.IntegerField(max_length=200)
    name=models.CharField(max_length=100)
    country_id=models.IntegerField(max_length=50)
    country_code=models.CharField(max_length=50)
    state_code=models.CharField(max_length=50,blank=True,null=True)
    # type=models.CharField(max_length=50,null=True,blank=True)
    latitude=models.DecimalField(max_digits=50,decimal_places=20,null=True)
    longitude=models.DecimalField(max_digits=50,decimal_places=20,null=True)

    def __str__(self):
        return self.name

class City(models.Model):
    
    name=models.CharField(max_length=100)
    state_id=models.IntegerField(max_length=100)
    state_code=models.CharField(max_length=100,null=True)
    country_id=models.IntegerField(max_length=100,null=True)
    country_code=models.CharField(max_length=100,null=True)
    latitude=models.DecimalField(max_digits=50,decimal_places=20,null=True)
    longitude=models.DecimalField(max_digits=50,decimal_places=20,null=True)
    wikiDataId=models.CharField(max_length=200,null=True)

    def __Str__(self):
        return self.name 


class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,max_length=50,null=True)
    state = models.ForeignKey(State1,on_delete=models.CASCADE,max_length=50,null=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE,max_length=50,null=True)
   
    def __str__(self):
        return self.user



