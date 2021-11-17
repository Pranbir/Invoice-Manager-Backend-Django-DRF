from rest_framework import views, response,status,viewsets
from . serializer import CustomerSerializer
from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.

#ashish

def index(request):
    return JsonResponse({"msg" : "API is working"})


# ashish
from .models import Customer

class CustomerAPI(viewsets.ModelViewSet):
    serializer_class=CustomerSerializer
    queryset=Customer.objects.all()