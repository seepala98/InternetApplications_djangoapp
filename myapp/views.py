from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound

from .forms import OrderForm, InterestForm
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
                order.product.stock -= order.num_units
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form':form, 'msg':msg, 'prodlist':prodlist})


def productdetail(request, prod_id):
    product = Product.objects.get(pk=prod_id)
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid() and int(form.cleaned_data['interested']) == 1:
            product.interested += 1
            product.save()
            msg = 'Order was successful'
            return render(request, 'myapp/order_response.html', {'msg': msg})
        else:
            msg = 'Some error occured in passing the form'
            return render(request,'myapp/order_response.html', {'msg': msg})
    else:
        form = InterestForm()
    return render(request, 'myapp/productdetail.html', {'form': form, 'product': product})