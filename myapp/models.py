from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def refill(self):
        self.stock += 100
        self.save()


class Client(User):
    PROVINCE_CHOICES = [
        (
            'AB', 'Alberta'
        ),
        (
            'MB', 'Manitoba'
        ),
        (
            'ON', 'Ontario'
        ),
        (
            'QC', 'Quebec'
        ),
    ]
    company = models.CharField(max_length=50, blank=True, null=True)
    shipping_address = models.CharField(max_length=300, null=True,
                                        blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES,
                                default='ON')
    interested_in = models.ManyToManyField(Category)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Order(models.Model):
    valid_value = [
        (
            0, 'Order Cancelled'
        ),
        (
            1, 'Order Placed'
        ),
        (
            2, 'Order Shipped'
        ),
        (
            3, 'Order Delivered'
        ),
    ]
    product = models.ForeignKey(Product, related_name='orders',
                                on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='orders',
                               on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=valid_value, default=1)
    status_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    def total_cost(self):
        return self.product.price * self.num_units
