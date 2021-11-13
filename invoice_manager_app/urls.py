from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import AppUserViewSet

router = DefaultRouter()
router.register("client", AppUserViewSet, basename="client")

urlpatterns = [
    path('', include(router.urls)),
]