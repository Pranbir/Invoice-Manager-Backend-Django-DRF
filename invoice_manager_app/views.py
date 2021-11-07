from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return JsonResponse({"msg" : "API is working"})