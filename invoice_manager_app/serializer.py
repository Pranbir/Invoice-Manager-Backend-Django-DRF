from django.db.models.base import Model
from django.db.models.fields import Field
from rest_framework import serializers
from django.contrib.auth.models import User
from .import models as Allmodels
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

#Abhishek----------

class customer_serializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200, )
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=100)


class tax_serializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    rate = serializers.FloatField()

class product_serializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=10, )
    price = serializers.FloatField()
    description = serializers.CharField(max_length=1000)


class order_serializer(serializers.Serializer):

    customer = serializers.IntegerField()
    date = serializers.DateField()
    due_date = serializers.DateField()
    discount_type = serializers.CharField()
    discount = serializers.FloatField()
    paid_status = serializers.CharField()
    total = serializers.FloatField()
    due_amount = serializers.FloatField()


class orderItem_serializer(serializers.Serializer):
    order = serializers.IntegerField()
    product=serializers.IntegerField()
    quantity = serializers.IntegerField()
    tax=serializers.IntegerField()
    unit_price = serializers.FloatField()
    total = serializers.FloatField()


class invoice_transaction_serializer(serializers.Serializer):
    
    date = serializers.DateField()
    amount = serializers.FloatField()
    description = serializers.CharField()
    payment_mode = serializers.IntegerField
    reference = serializers.CharField()

#=====================model serializer class ==========================

class order_modelserializer(serializers.ModelSerializer):
    class Meta:
        model = Allmodels.Order
        fields ='__all__'

class customer_modelserializer(serializers.ModelSerializer):
    orders=order_modelserializer(read_only=True,many=True)    #you have to defined in the primary table that you are going to give 
    class Meta:
        model=Allmodels.Customer
        fields ='__all__'


#=================invoice Transaction==================================

class invoice_transaction_Modelserializer(serializers.ModelSerializer):
    class Meta:
        model=Allmodels.InvoiceTransaction
        fields ='__all__'

class product_Modelserializer(serializers.ModelSerializer):
    invoice=invoice_transaction_Modelserializer(read_only=True,many=True)
    class Meta:
        model=Allmodels.Product
        fields ='__all__'

class payment_mode_Modelserializer(serializers.ModelSerializer):
    invoice=invoice_transaction_Modelserializer(read_only=True,many=True)
    
    class Meta:
        model=Allmodels.PaymentMode
        fields ='__all__'        