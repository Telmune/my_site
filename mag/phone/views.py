import stripe.checkout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, OrderDetail
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    page_obj = items = Product.objects.all()

    item_name = request.GET.get("search")
    if item_name != "" and item_name is not None:
        page_obj = items.filter(name__icontains=item_name)

    paginator = Paginator(page_obj, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "phone/index.html", context)

class ProductListView(ListView):
    model = Product
    template_name = "phone/index.html"
    context_object_name = "items"
    paginate_by = 2


# def indexItem(request, my_id):
#     item = Product.objects.get(id=my_id)
#     context = {
#         'item': item
#     }
#     return render(request, "phone/detail.html", context=context)

class ProductDetailView(DetailView):
    model = Product
    template_name = "phone/detail.html"
    context_object_name = "item"
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context["stripe_publishabke_key"] = settings.STRIPE_PUBLISHABLE_KEY
        return context
@login_required
def add_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES['upload']
        seller = request.user
        item = Product(name=name,price=price, description=description,image=image, seller=seller)
        item.save()
    return render(request,"phone/additem.html")

def update_item(request,my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.description = request.POST.get("description")
        item.image = request.FILES.get('upload', item.image)
        item.save()
        return redirect("/phone/")
    context = {
        'item': item
    }
    return render(request, "phone/updateitem.html", context)

def delete_item(request,my_id):
    item = Product.objects.get(id=my_id)
    if request.method == "POST":
        item.delete()
        return redirect("/phone/")
    context = {
        'item': item
    }
    return render(request, "phone/deleteitem.html", context)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("phone:index")

@csrf_exempt
def create_checkout_session(request, id):
    product = get_object_or_404(Product, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                    },
                    "unit_amount": int(product.price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("phone:success"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("phone:failed")),
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )

    order = OrderDetail()
    order.product = product
    order.stripe_payment_intent = checkout_session["payment_intent"]
    order.amount = int(product.price * 100)
    order.save()

class PaymentSuccessViews(TemplateView):
    template_name = "phone/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        session = stripe.checkout.Session.retrive(session_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = get_object_or_404(OrderDetail,stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)

class PaymentFailedViews(TemplateView):
        template_name = "phone/payment_failed.html"