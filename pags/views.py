from django.shortcuts import render
from products.models import Product


def index(request):
    count = {'products': Product.objects.all()}

    return render(request, 'pags/index.html', count)


def about(request):
    return render(request, 'pags/about.html')


def coffee(request):
    return render(request, 'pags/coffee.html')