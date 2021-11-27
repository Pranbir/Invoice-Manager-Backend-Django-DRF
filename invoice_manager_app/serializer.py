from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PaymentMode
from .models import Tax

# ashish

from .models import Customer,Product
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

#arvind
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


#prachi 

# PaymentMode Serializer

class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = '__all__'

# TaxMode Serializer

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'