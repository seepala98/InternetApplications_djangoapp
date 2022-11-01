from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from .models import Category, Product, Client, Order
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    prod_list = Product.objects.all().order_by('-price')[:5]
    response = HttpResponse()
    heading1 = '<p>' + 'List of categories: ' + '</p>'
    response.write(heading1)
    for category in cat_list:
        para = '<p>' + str(category.id) + ': ' + str(category) + '</p>'
        response.write(para)
    heading2 = '<p>' + 'List of products: ' + '</p>'
    response.write(heading2)
    for product in prod_list:
        para = '<p>' + str(product) + ': $' + str(product.price) + '</p>'
        response.write(para)
    return response


def about(request):
    response = HttpResponse()
    heading = '<p>' + 'This is an Online Store APP.' + '</p>'
    response.write(heading)
    return response


def detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    response = HttpResponse()
    heading = '<p>' + 'Category: ' + str(category) + '</p>'
    response.write(heading)
    cat_list = Category.objects.all().order_by('id')[:10]
    for category in cat_list:
        if category.id == int(cat_no):
            para = '<p>' + 'Warehouse Location: ' + str(category.warehouse) + '</p>'
            response.write(para)
    prod_list = Product.objects.filter(category=cat_no)
    heading2 = '<p>' + 'List of products: ' + '</p>'
    response.write(heading2)
    for product in prod_list:
        para = '<p>' + str(product) + ': $' + str(product.price) + '</p>'
        response.write(para)
    return response
