from rest_framework import serializers


# ashish
from .models import Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# ----

# vivek


# ----