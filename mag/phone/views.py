from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def index(request):
    items = Product.objects.all()
    context = {
        'items': items
    }
    return render(request, "phone/index.html", context)


def indexItem(request, my_id):
    item = Product.objects.get(id=my_id)
    context = {
        'item': item
    }
    return render(request, "phone/detail.html", context=context)
