from datetime import datetime

from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import OrderForm, InterestForm, LoginForm
from .models import Category, Product, Client, Order
from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    if request.session.get('last_login') is None:
        last_login = request.session.get('last_login')
        last_login_flag = True
    else:
        last_login = 'Your last login was more than one hour ago'
        last_login_flag = False
    cat_list = Category.objects.all().order_by('id')[:10]
    prod_list = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'prod_list': prod_list, 'last_login': last_login,
                                                'last_login_flag': last_login_flag})


def about(request):
    if request.COOKIES.get('about_visits'):
        visits = int(request.COOKIES.get('about_visits'))
        visits += 1
    else:
        visits = 1
    response = render(request, 'myapp/about.html', {'visits': visits})
    response.set_cookie('about_visits', visits, max_age=300)
    return response


def detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    cat_list = Category.objects.all().order_by('id')[:10]
    prod_list = Product.objects.filter(category=cat_no)
    return render(request, 'myapp/detail.html',
                  {'cat_no': cat_no, 'cat_list': cat_list, 'prod_list': prod_list})


def products(request):
    prod_list = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prod_list': prod_list})


@login_required
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
                order.product.save()
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


@login_required
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
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = InterestForm()
    return render(request, 'myapp/productdetail.html', {'form': form, 'product': product})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details")
    else:
        form = LoginForm()
        return render(request, 'myapp/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def myorders(request):
    current_user = request.user
    msg = ""
    if not current_user.is_active:
        msg = "You are not a Registered Client"
        return render(request, 'myapp/myorders.html', {'msg': msg})
    else:
        order_list = Order.objects.filter(client__id=current_user.id)
        interested_in = Product.objects.filter(interested__gt=0)
        return render(request, 'myapp/myorders.html', {'msg': msg, 'firstname': current_user.first_name,
                                                       'lastname': current_user.last_name,
                                                       'order_list': order_list, 'interested_in': interested_in})
