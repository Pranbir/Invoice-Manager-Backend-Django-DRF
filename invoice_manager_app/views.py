from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets 
from .serializers import UserSerializer
from invoice_manager_app.models import AppUser
from django.core.exceptions import PermissionDenied

# Create your views here.
class AppUserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = AppUser.objects.all()

    def get_queryset(self):
        return self.queryset.filter()
    
    def perform_create(self, serializer):
        serializer.save()