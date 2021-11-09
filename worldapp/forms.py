from .models import Address
from django import forms


class UserAddress(forms.ModelForm):
    class Meta: 
      model=Address  
      fields=['user','country','state','city']  
     