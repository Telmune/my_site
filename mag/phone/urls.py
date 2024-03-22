from django.contrib import admin
from django.urls import path, include
from phone.views import *
from .views import PaymentFailedViews, PaymentSuccessViews

app_name = "phone"

urlpatterns = [
    # path("", index, name='index'),
    path("", ProductListView.as_view(), name='index'),
    # path("<int:my_id>/", indexItem, name="detail"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    path("additem/", add_item, name="add_item"),
    path("updateitem/<int:my_id>/", update_item, name="update_item"),
    path("deleteitem/<int:pk>/", ProductDeleteView.as_view(), name="delete_item"),
    path("success/", PaymentSuccessViews.as_view(), name="success"),
    path("failed/", PaymentFailedViews.as_view(), name="failed"),
    path("api/checkout-session/<int:id>/", update_item, name="api_checkout_session"),
]
