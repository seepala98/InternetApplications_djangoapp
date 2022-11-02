from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
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
