from django.contrib import admin
from django.urls import path
from .views import *
# from worldapp.views import Add

urlpatterns = [
    path('admin/', admin.site.urls),
    path('country', Countryshow,name="countryview"),
    
    path('load-state/', Stateshow,name="ajax_load_state"),
    path('load-city/', Cityshow,name="ajax_load_city"),
    
    path('add/',add,name="add"),
    path('address/',Address.as_view(),name="address"),
    path('',Signup.as_view(),name="signup"),     
    path('login',Login.as_view(),name="login"),     
    path('logout',logout,name="logout"),     
       
]