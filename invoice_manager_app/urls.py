
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
#Abhishek
order_router=routers.DefaultRouter()
order_router.register('orders',views.order_viewset,basename="order_viewset")
invoice_router=routers.DefaultRouter()
invoice_router.register('invoices',views.invoice)


urlpatterns = [
    path('', views.index, name="api_working" ),
    path('',include(router.urls)),
    path('',include(Register_router.urls)),
    path('login',views.LoginView.as_view()),
    path('logout',knox_views.LogoutView.as_view()),
    path('invoice/',views.invoice_details.as_view(),name='invoice_page'),
    path("invoice/<int:invoice_id>",views.invoice_details.as_view(),name='invoice_page_with_id'),
    path("orderItems/",views.order_item.as_view(),name='order_details'),
    path("orderItems/<int:orderid>",views.order_item.as_view(),name='order_details_with_id'),
    path("orders/<int:order>",views.orders.as_view(),name="orders_with_id"),
    path("orders/",views.orders.as_view(),name="allorders"),
    path("viewset_orders",include(order_router.urls)),
    path("modelViewset_invoices",include(invoice_router.urls))
]
