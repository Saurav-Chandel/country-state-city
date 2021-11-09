from django.shortcuts import render,HttpResponse,redirect
from .models import Country,State1,City,User,Address
import csv
import json

#
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.core.exceptions import BadRequest, ValidationError
#token generate imports
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from rest_framework.permissions import AllowAny,IsAuthenticated
# Create your views here.
# from main.settings import *
from .serializers import *
import jwt
from worldproj import settings
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import login,authenticate

#lsignup and login view.
from django.shortcuts import render, redirect ,HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import  check_password
from worldapp.models import User
from django.views import View


#
import pytz
from datetime import datetime, timedelta
# from django.core.mail import EmailMultiAlternatives, send_mail
import base64
import random
# import pyotp
import json

class RegisterView(APIView):
    permission_classes=(AllowAny,)
    
    def post(self,request):
        try:
            user=User.objects.get(email=request.data['email'])     
            return Response({"data":None,"message":"Email Already Exist"},status=status.HTTP_400_BAD_REQUEST) 
        except:
            data=request.data.copy()
            data['email'] =request.data['email'].lower()
            # data['otp']=otp
            # print(data)
            serializer=UserSignupSerializer(data=data)
            # print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

class AddressView(APIView):
    permission_classes=(AllowAny,)         
    def post(self,request):
        user=request.session.get('user')
        data=request.data.copy() 
        print(data)
        # user=request.data['user']
        user = User.objects.get(id = user)
        data['user']=user.id   #it does not take string value. thats why it gives an error.
        print(user)
        
        serializer=AddressSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 


from django.views import View        
class Signup(View):
    def post(self, request):
        return render(request, 'signup.html')

class LoginView(APIView):
    permission_classes=(AllowAny,)

    def post(self,request):
        if "email" in request.data and "password" in request.data:
            email=request.data['email']
            email=email.lower()
            password=request.data['password']
            try:
                user=User.objects.get(email=email) #agr email match krti h db vali email se.
            except User.DoesNotExist:
                return Response({"data": None,"message": "User Does Not Exist"},status = status.HTTP_400_BAD_REQUEST)
            
            if user.check_password(password): #check password if it matches.
                login(request, user)
                serializer=UserLoginSerializer(user)
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY) 
                user_details = serializer.data                   
                user_details["token"] = token
                  
                return Response({
                            "data": user_details,
                            "code": status.HTTP_200_OK,
                            "message": "Login SuccessFully",
                        },status = status.HTTP_200_OK)
            else:
                return Response({
                        "data": None,
                        "code": status.HTTP_400_BAD_REQUEST,
                        "message": "Invalid Credentials",
                        },status = status.HTTP_400_BAD_REQUEST)

 
def Countryshow(request):
    email=request.session.get('email')
    user=request.session.get('user')
    country=Country.objects.all()
    data={
        'email':email,
        'user':user,
        "countries":country,
        
        }
    # postdata=request.POST
    return render(request,"html/index.html",data)


def Stateshow(request):
    country_id=request.GET.get('country')
     # print("country_id",country_id)
    state=State1.objects.filter(country_id=country_id)    #.values("name").distinct().order_by('name')
    # print("states:",state)
    return render(request,"html/state_dropdown_ajax.html",{"states":state}) 


def Cityshow(request):
    state_id=request.GET.get('state')
    # print("state_id",state_id)
    city=City.objects.filter(state_id=state_id)    #.values("name").distinct().order_by('name')
    # print("cities",city)
    return render(request,"html/city_dropdown_ajax.html",{"cities":city}) 


def add(request):
        # user = User.objects.get(id = request.user.id) 

        if request.method=="POST":
            
        #    if request.POST.get('country'):
                country=request.POST.get('country')
                print(country)
            #   savevalue=Address()
            #   savevalue.name=request.POST.get('country')
            #   savevalue.save()
            #   return render(request,'index.html')
        # else:
            # return HttpResponse("hello")
            # return redirect("countryview")
class Address(View):
    def get(self,request):
        return redirect("countryview")
    def post(self,request): 
        country=request.POST.get('country')
        
        print(country)


class Signup(View):
    def get(self, request):
        return render(request, 'html/signup.html')

    def post(self, request):
        postData = request.POST
        email = postData.get('email')
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        password = postData.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        error_message = None

        user = User(email=email,
                    first_name=first_name,
                            last_name=last_name,
                            password=password)
        error_message = self.validateUser(user)

        if not error_message:
            # print(first_name, last_name,email, password)
            user.password = make_password(user.password)  # this line makes the password hash.
            user.save()
            return redirect('login')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'html/signup.html', data)

    def validateUser(self, user):
        error_message = None;
        if (not user.first_name):
            error_message = "First Name Required !!"
        elif len(user.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not user.last_name:
            error_message = 'Last Name Required'
        elif len(user.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'

        elif len(user.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(user.email) < 5:
            error_message = 'Email must be 5 char long'
        elif user.isExists():
            error_message = 'Email Address Already Registered..'
        # saving
        return error_message    

class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'html/login.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.get_user_by_email(email)
        error_message = None
        if user:
            flag = check_password(password, user.password)
            if flag:
                request.session['user'] = user.id
                request.session['email'] = user.email
                # print(email)
                
                # print(data)
                # return render(request, 'index.html', data)

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    # country=Country.objects.all()
                    # data={
                    # 'email':email,
                    # 'user':user,
                    # 'countries':country
                    # }
                    return redirect('countryview')  
                    # return render(request,'index.html',data)
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'
        
        # print(data)
        # print(email, password)
        return render(request, 'html/login.html', {'error': error_message,'email':email,'user':user})

def logout(request):
    request.session.clear()
    return redirect('login')        
        







# class Login(View):
#     def login(request):
#         c = {}
#         c.update(csrf(request))
#         return render(request, 'login.html', c)

#     def auth_view(request):
#         email = request.POST.get('email', '')
#         password = request.POST.get('password', '')
#         user = auth.authenticate(email = email, password = password)      

#         if user is not None:
#             auth.login(request, user)
#             return HttpResponseRedirect('/accounts/loggedin')
#         else:
#             return HttpResponseRedirect('/accounts/invalid')




        

            

# rom django.views.generic import TemplateView
# class ApiLoginView(TemplateView):
#     template_name = 'signup.html'
    
#     def post(self,request):
#         email = request.POST.get('email')
#         print(email)
#         firstname=request.POST.get('firstname')
#         lastname=request.POST.get('lastname')
#         password = request.POST.get('password')
#         print(password)
        
#         API_URL = 'http://localhost:8000/api/signup/'
#         parameter = {
#             # 'authToken':API_KEY,
#             'email':email,
#             'firstname':firstname,
#             'lastname':lastname,
#             'password':password
#         }
#         r = session.post(url = API_URL, params=parameter)
#         print(r.json()['code'])
#         return render(request,'signup.html') f    




# this function exports the city data into database.
# def xyz(request):
#     csvFilePath = r"worldapp/cities.csv"

#     data=[]

#     with open(csvFilePath,encoding='utf-8') as csvFile:
#         csvReader=csv.DictReader(csvFile)
#         a = 0
#         for rows in csvReader:
#             a = a+1
#             print(a)
#             City.objects.create(state_id = rows.get("state_id",None),state_code=rows.get("state_code",None),name=rows.get("name",None),country_id =rows.get("country_id",None),country_code=rows.get('country_code',None),latitude=rows.get('latitude',None),longitude=rows.get('longitude',None),wikiDataId=rows.get('wikiDataId',None))
#     return HttpResponse(data) 










    




