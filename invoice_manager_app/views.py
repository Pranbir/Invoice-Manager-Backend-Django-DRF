from rest_framework import views, response,status,viewsets
from . serializer import CustomerSerializer
from django.http.response import JsonResponse
from django.shortcuts import render
from .models import Customer


# Create your views here.
def index(request):
    return JsonResponse({"msg" : "API is working"})


# ashish
class CustomerAPI(viewsets.ModelViewSet):
    serializer_class=CustomerSerializer
    queryset=Customer.objects.all()