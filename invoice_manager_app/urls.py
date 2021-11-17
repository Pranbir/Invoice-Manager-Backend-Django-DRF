
from django.urls import path, include
from . import views
from rest_framework import routers

router =routers.DefaultRouter()
# ashish
router.register('customer',views.CustomerAPI,basename='customer')
# vivek
# xxxxxxx

urlpatterns = [
    path('', views.index, name="api_working" ),
        path('',include(router.urls)),


]
