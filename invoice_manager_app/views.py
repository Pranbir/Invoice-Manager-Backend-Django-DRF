from rest_framework import  response,status,viewsets,permissions,serializers,views,filters
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
from . import models as Allmodels
from .import serializer

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


#Abhishek(using ApiViews) ----------------------------------------------------------------

class invoice_details(views.APIView):
    # serializer_class=serializer.helloSerializers
    def get(self, request, invoice_id=None):

        if invoice_id is not None:
            # used filter instead of get ,helps eliminate error with null query set.
            try:
                invoiceObject = Allmodels.InvoiceTransaction.objects.get(
                    id=invoice_id)
                invoiceObject={invoiceObject} 
                invoiceObject1 = {}
                for key, i in enumerate(invoiceObject):
                    order = Allmodels.Order.objects.get(id=i.order_id)
                    order_item = Allmodels.OrderItems.objects.get(
                        order_id=i.order_id)

                    invoiceObject1[key] = {
                        "id": i.id,
                        "date": order.date,
                        "due_date": order.due_date,
                        "status": order.paid_status,
                        "amount": i.amount,
                        "paid_total": order.total,
                        "tax": order_item.tax.name,
                        "Due amount": order.due_amount,
                        "discount": order.discount,
                        "payment_mode": i.payment_mode.name,
                        "order": i.order.customer.name,

                    }
                invoiceObjectlist = list(invoiceObject1.values())
                if invoiceObjectlist.__len__() == 0:
                    invoiceObject = "No invoice with that invoice id "
                else:
                    invoiceObject = invoiceObjectlist
            except:
                return(response.Response(status=status.HTTP_400_BAD_REQUEST))

        else:

            invoiceObject = Allmodels.InvoiceTransaction.objects.all()
            invoiceObject1 = {}
            for key, i in enumerate(invoiceObject):
                order = Allmodels.Order.objects.get(id=i.order_id)
                order_item = Allmodels.OrderItems.objects.get(
                    order_id=i.order_id)

                invoiceObject1[key] = {
                    "id":i.id,
                    "invoice_number": i.id,
                    "status": order.paid_status,
                    "client": order.customer.name,
                    "due_date": order.due_date,
                    "amount": i.amount,
                    "paid_total": order.total,
                    "Due amount": order.due_amount,


                }

            invoiceObject = list(invoiceObject1.values())

        return (response.Response({"invoice_details": invoiceObject}))

    
class order_item(views.APIView):
    order_serializer_class=serializer.orderItem_serializer
    

    def get(self, request, orderid=None):

        if orderid is None:
            orderItemObject = Allmodels.OrderItems.objects.all()
            orderItem = {}
            for key, i in enumerate(orderItemObject):
                orderItem[key] = {
                    "id":i.id,
                    "order": i.order.customer.name,
                    "product": i.product.name,
                    "quantity": i.quantity,
                    "tax": i.tax.name,
                    "unit_price": i.unit_price,
                    " total": i.total,
                }
            orderItem = list(orderItem.values())
            print(orderItem)

        else:

            try:
                orderItem = Allmodels.OrderItems.objects.get(id=orderid)

                orderItem = model_to_dict(orderItem)
            except:
                orderItem = ["Key you enter is not found"]

        return(response.Response({"order_item": orderItem}))


    def post(self,request,orderid=None):
        if orderid is not None:
            return(response.Response("you cant create new object in existing object"))
        
        else:
            order_item_serializer=self.order_serializer_class(data=request.data)
        
            if order_item_serializer.is_valid():

                order=order_item_serializer.validated_data.get('order')
                product=order_item_serializer.validated_data.get('product')
                quantity =order_item_serializer.validated_data.get('quantity')
                tax=order_item_serializer.validated_data.get('tax')
                unit_price =order_item_serializer.validated_data.get('unit_price')
                total =order_item_serializer.validated_data.get('total')

                try:
                    order_instance=Allmodels.Order.objects.get(id=order)
                    product_instance=Allmodels.Product.objects.get(id=product)
                    tax_instance=Allmodels.Tax.objects.get(id=tax)
                except:
                    return(response.Response("Problem with order_item instance "))
                
                Allmodels.OrderItems.objects.create(order=order_instance,product=product_instance,quantity=quantity,
                                                        tax=tax_instance,unit_price=unit_price,total=total).save()

                return(response.Response("OrderItem Data submitted successfully!"))
            else:
                return(response.Response("you are trying to submite incomplete data or data is not in correct form"))    
    def patch(self,request,orderid=None):
        if orderid is not None:
            order_item_serializer=self.order_serializer_class(data=request.data,partial=True)
            try:    
                orderItem=Allmodels.OrderItems.objects.get(id=orderid)
            except:
                return(response.Response("Order item you are looking for does not exist"))
            
            if order_item_serializer.is_valid():
                order=order_item_serializer.validated_data.get('order')
                product=order_item_serializer.validated_data.get('product')
                quantity =order_item_serializer.validated_data.get('quantity')
                tax=order_item_serializer.validated_data.get('tax')
                unit_price =order_item_serializer.validated_data.get('unit_price')
                total =order_item_serializer.validated_data.get('total')
                


                if order is not None:
                    try:
                        order_instance=Allmodels.Order.objects.get(id=order)
                        orderItem.order=order_instance

                    except:
                        return(response.Response("this order does not exist in order table"))
                
                if product is not None:
                    try:
                        product_instance=Allmodels.Product.objects.get(id=product)
                        orderItem.product=product_instance

                    except:
                        return(response.Response("this product does not exist in product table"))
                     
                
                if quantity is not None:
                    
                    orderItem.quantity=quantity
                        
                if tax is not None:
                    try:
                        tax_instance=Allmodels.Tax.objects.get(id=tax)
                        orderItem.tax=tax_instance

                    except:
                        return(response.Response("this tax does not exist in tax table"))
                if unit_price is not None:
                    
                    orderItem.unit_price=unit_price    

                if total is not None:
                    orderItem.total=total

                orderItem.save()   
                return(response.Response("Order Item Table partially updated successfully "))             
            else:
                return(response.Response("you are trying to submite data which is not in correct form"))
        else:
            return(response.Response("For Updating existing data you need to enter order id"))
    def delete(self, request,orderid=None):
            try:
                orderItem=Allmodels.OrderItems.objects.get(id=orderid)
            except:
                return(response.Response("Item you are looking for does not exist in orderItem Table"))

            orderItem.delete()    
            return(response.Response("Item successfully deleted from OrderItem Table"))


class orders(views.APIView):
    order_serializer_class = serializer.order_serializer
    def get(self,request,order=None):
        if order is not None:
            try:
                order=Allmodels.Order.objects.get(id=order)
                order=model_to_dict(order)
                
            except:
                return(response.Response({"Order Does not found or Does not exist"}))

        else:
            order=Allmodels.Order.objects.all()
            print(order)
            Allorder={}
            for key,i in enumerate(order):
                Allorder[key]={
                "id":i.id,
                "customer" : i.customer.name,
                "date" :i.date,
                "due_date": i.due_date,
                "discount_type" : i.discount_type,
                "discount" : i.discount,
                "paid_status" :i.paid_status ,
                "total" :i.total, 
                "due_amount" :i.due_amount }
            order=list(Allorder.values())    

        return(response.Response({"Orders":order}))

    
    def post(self, request):
       
        print("this is request =====>",request.data)
        order_serializer = self.order_serializer_class(data=request.data)
        
        if order_serializer.is_valid():
            customer = order_serializer.validated_data.get('customer')
            date = order_serializer.validated_data.get('date')
            due_date = order_serializer.validated_data.get('due_date')
            discount_type = order_serializer.validated_data.get('discount_type')
            discount = order_serializer.validated_data.get('discount')
            paid_status = order_serializer.validated_data.get('paid_status')
            total = order_serializer.validated_data.get('total')
            due_amount = order_serializer.validated_data.get('due_amount')
        
            try:
                customer_instance=Allmodels.Customer.objects.get(id=customer)
                Allmodels.Order.objects.create(customer=customer_instance, date=date, due_date=due_date, discount_type=discount_type,
                                            discount=discount, paid_status=paid_status, total=total, due_amount=due_amount).save()
                return(response.Response("data submitted successfully in order table !!!!!!"))
            except:
                return(response.Response("Customer Does not exist !"))
        else:
            return(response.Response("you are trying to submite incomplete data or data is not in correct form"))


    def patch(self ,request,order=None):
        if order is not None:
            order_instance=Allmodels.Order.objects.get(id=order)
            order_serializer = self.order_serializer_class(data=request.data,partial=True)
            print("order Object==================>",order_instance)
            if order_serializer.is_valid():
                customer = order_serializer.validated_data.get('customer')
                date = order_serializer.validated_data.get('date')
                due_date = order_serializer.validated_data.get('due_date')
                discount_type = order_serializer.validated_data.get('discount_type')
                discount = order_serializer.validated_data.get('discount')
                paid_status = order_serializer.validated_data.get('paid_status')
                total = order_serializer.validated_data.get('total')
                due_amount = order_serializer.validated_data.get('due_amount')
                #fetching data from seraillizer.
                
                if customer is not None:
                    try:
                        customerObj=Allmodels.Customer.objects.get(id=customer)
                        order_instance.customer=customerObj
                    except:
                        return(response.Response("Customer is not available or not found in DB"))
                if date is not None:
                    order_instance.date = date = date
                if due_date is not None:
                    order_instance.due_date = due_date

                if discount_type is not None:
                    order_instance.discount_type = discount_type
                if discount is not None:
                    order_instance.discount = discount

                if paid_status is not None:
                    order_instance.paid_status = paid_status
                if total is not None:
                    order_instance.total = total
                if due_amount is not None:
                    order_instance.due_amount = due_amount
                order_instance.save()
                return(response.Response("The partial data is updated in the DB"))
            else:
                return(response.Response("Problem fetchig data"))
        else:
            return(response.Response("Need order id to update existing data"))

        return(response.Response("this is path method"))


    def delete(self,request,order=None):
        if order is not None:
            Allmodels.Order.objects.get(id=order).delete()
            return(response.Response("The data related to that id is deleted successfully !!"))
        else:
            return(response.Response("Need order id to delete the data"))    

# ==============================invoice using Model viewset =================================
class invoice(viewsets.ModelViewSet):




    serializer_class= serializer.invoice_transaction_Modelserializer
    queryset=Allmodels.InvoiceTransaction.objects.all()
    print( "queryset",queryset)      
    filter_backends=(filters.SearchFilter,)
    search_fields=('id','amount','description')
    ordering_fields=['amount','id']


    


# app user - Rishi
from . import models
class AppUser(viewsets.ModelViewSet):
    serializer_class=serializer.AppSerializer
    queryset=models.AppUser.objects.all()