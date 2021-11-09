from django.contrib import admin
from django.urls import path,include




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('worldapp.urls') ),
    path('api/',include('worldapp.api_urls') )
    
]
