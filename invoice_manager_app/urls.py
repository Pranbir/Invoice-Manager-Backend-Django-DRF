
from django.urls import path, include
from . import views
from rest_framework import routers
from knox import views as knox_views

router =routers.DefaultRouter()
Register_router= routers.DefaultRouter()
Register_router.register('register',views.register,basename='register')
# ashish
router.register('customer',views.CustomerAPI,basename='customer')
# vivek
# xxxxxxx
#arvind
router.register('product',views.ProductViewSet,basename='Product')

# Prachi

router.register('paymentmode',views.PaymentModeAPI,basename='paymentmode')

router.register('tax', views.TaxAPI, basename='tax')


urlpatterns = [
    path('', views.index, name="api_working" ),
    path('',include(router.urls)),
    path('',include(Register_router.urls)),
    path('login',views.LoginView.as_view()),
    path('logout',knox_views.LogoutView.as_view())
]
