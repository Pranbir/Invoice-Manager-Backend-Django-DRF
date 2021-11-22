from rest_framework import serializers
from django.contrib.auth.models import User

# ashish

from .models import Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
# ----

# vivek

# Registration Serializer
class userserializers(serializers.Serializer):
    first_name=serializers.CharField(max_length=20)
    last_name=serializers.CharField(max_length=20)
    username=serializers.CharField(max_length=20)
    password=serializers.CharField(max_length=20)

# Login Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','username','password']
# ----