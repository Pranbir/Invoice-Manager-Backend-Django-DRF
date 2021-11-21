[1mdiff --git a/invoice_manager_app/views.py b/invoice_manager_app/views.py[m
[1mindex 5cf6aff..364a9db 100644[m
[1m--- a/invoice_manager_app/views.py[m
[1m+++ b/invoice_manager_app/views.py[m
[36m@@ -2,18 +2,15 @@[m [mfrom rest_framework import views, response,status,viewsets[m
 from . serializer import CustomerSerializer[m
 from django.http.response import JsonResponse[m
 from django.shortcuts import render[m
[32m+[m[32mfrom .models import Customer[m
 [m
[31m-# Create your views here.[m
[31m-[m
[31m-#ashish[m
 [m
[32m+[m[32m# Create your views here.[m
 def index(request):[m
     return JsonResponse({"msg" : "API is working"})[m
 [m
 [m
 # ashish[m
[31m-from .models import Customer[m
[31m-[m
 class CustomerAPI(viewsets.ModelViewSet):[m
     serializer_class=CustomerSerializer[m
     queryset=Customer.objects.all()[m
\ No newline at end of file[m
