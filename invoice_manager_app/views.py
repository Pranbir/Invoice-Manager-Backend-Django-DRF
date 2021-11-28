from rest_framework import  response,status,viewsets,permissions,serializers
from . serializer import CustomerSerializer,ProductSerializer
from django.http.response import JsonResponse
from .models import Customer,Product
from django.contrib.auth.models import User
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.forms.models import model_to_dict
from . serializer import userserializers
from rest_framework.generics import get_object_or_404
from . serializer import PaymentModeSerializer
from .models import PaymentMode
from . serializer import TaxSerializer
from .models import Tax

# Create your views here.
def index(request):
    return JsonResponse({"msg" : "API is working"})


# ashish
class CustomerAPI(viewsets.ModelViewSet):
    serializer_class=CustomerSerializer
    queryset=Customer.objects.all()


#vivek
class register(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,) 
    """ 
    Format for registration
    {
        "first_name":"first_name",
        "last_name":"last_name",
        "username":"username",
        "password":"password"
    }
    """
    def create(self,request):
        serializers_class=userserializers
        serializers_class=serializers_class(data=request.data)
        if serializers_class.is_valid():
            user=User.objects.create(
                first_name=serializers_class.validated_data.get('first_name'),
                last_name=serializers_class.validated_data.get('last_name'),
                username=serializers_class.validated_data.get('username'),
                is_staff=True,     #
                is_active=True,    #  these fields can be changed with what front end team wants.
                is_superuser=True  #
            )
            user.set_password(serializers_class.validated_data.get('password'))
            user.save()
            return response.Response({'message':f'created user {user.username}'})
        else:
            return response.Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        try:
            user=User.objects.get(pk=pk)
            username=user.username
            user.delete()
            return response.Response({'message':f'user {username} account deleted'})
        except:
            return response.Response({'message':'no user found or user deleted'})

#vivek
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    """ 
    Format to login
    {
        "username":"username",
        "password":"password"
    }
    """

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        userss=list(User.objects.filter(username=serializer.validated_data.get('username')))
        temp_list=super(LoginView, self).post(request, format=None)
        model=model_to_dict(userss[0])
        print(model)
        user_model={"id":model['id'],"username":model['username']}
        temp_list.data['user']=user_model
        return response.Response({"data":temp_list.data})

#arvind
class ProductViewSet(viewsets.ViewSet):
    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    def list(self,request):
        serializer=self.serializer_class(self.queryset,many=True)
        return response.Response(serializer.data)
    
    def retrieve(self,request,pk=None):
        product= get_object_or_404(self.queryset,pk=pk)
        serializer=self.serializer_class(product)
        return response.Response(serializer.data)
    
    def create(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)
    
    def update(self,request,pk=None):
        product= get_object_or_404(self.queryset,pk=pk)
        serializer=self.serializer_class(product,request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)
    
    def partial_update(self,request,pk=None):
        product= get_object_or_404(self.queryset,pk=pk)
        serializer=self.serializer_class(product,request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)
    def destroy(self,request,pk=None):
        product= get_object_or_404(self.queryset,pk=pk)
        product.delete() 
        return response.Response({'message':'Succesfully Deleted'},status=status.HTTP_200_OK)

# Prachi

class PaymentModeAPI(viewsets.ModelViewSet):
    serializer_class=PaymentModeSerializer
    queryset=PaymentMode.objects.all()
   



class TaxAPI(viewsets.ModelViewSet):
    serializer_class=TaxSerializer
    queryset=Tax.objects.all()