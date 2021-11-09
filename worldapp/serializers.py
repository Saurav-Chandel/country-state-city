from rest_framework import serializers
from .models import User,Address

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password']
        extra_kwargs = {
                'first_name': {'required': True},
                'last_name': {'required': True}
                }
    def create(self, validated_data):
        user = User.objects.create(
            
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user  

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','first_name','last_name']  


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields=['country','state','city','user']


