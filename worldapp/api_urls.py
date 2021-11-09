from django.contrib import admin
from django.urls import path
from .views import *
# from worldapp.views import Add


urlpatterns = [
    #API
    path("signupapi/", RegisterView.as_view(), name="signupapi"),
    path("loginapi/", LoginView.as_view(), name="loginapi"),
    path("Address/", AddressView.as_view(), name="AddressView"),
]
