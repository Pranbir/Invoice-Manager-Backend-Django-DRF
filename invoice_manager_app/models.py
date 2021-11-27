from django.db import models
from django.contrib.auth.models import User

# Create your models here.

choice_role = [('admin', 'admin'), ('staff', 'staff')]
paid_status = [('paid', 'paid'), ('unpaid', 'unpaid'), ('partial', 'partial')]
discount_type = [('percentage', 'percentage'), ('amount', 'amount')]


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    contact_no = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=5, choices=choice_role, default='staff')

    def __str__(self):
        return self.user.username


#ashsih
class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True)
    price = models.FloatField()
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField(max_length=100)
    rate = models.FloatField()

    def __str__(self):
        return self.name


class PaymentMode(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField( auto_now_add=True)
    due_date = models.DateField(null=True)
    discount_type = models.CharField(max_length=10, choices=discount_type, default='percentage')
    discount = models.FloatField(default=0)
    paid_status = models.CharField(max_length=15, choices=paid_status, default='paid')
    total = models.FloatField()
    due_amount = models.FloatField(null=True, default=0)


    def __str__(self):
        return self.customer.name


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True)
    unit_price = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return self.product.name


class InvoiceTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField()
    description = models.TextField(null=True)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True)
    reference = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.order.customer.name