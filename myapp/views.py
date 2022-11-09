from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound

from .forms import OrderForm
from .models import Category, Product, Client, Order
from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    prod_list = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'prod_list': prod_list})


def about(request):
    return render(request, 'myapp/about.html')


def detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    cat_list = Category.objects.all().order_by('id')[:10]
    prod_list = Product.objects.filter(category=cat_no)
    return render(request, 'myapp/detail.html',
                  {'cat_no': cat_no, 'cat_list': cat_list, 'prod_list': prod_list})


def products(request):
    prod_list = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prod_list': prod_list})


# Define another view place_order(request) in your views.py file. When the user goes to url
# myapp/place_order, the view will display a list of products in the database along with their
# prices and provide a form for the user place an order for a product

def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have suffucient stock to fill your order.'
            return render(request, 'myapp/place_order.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/place_order.html', {'form': form, 'msg': msg, 'prodlist': prodlist})