from django.contrib import admin
from django.urls import path, include
from phone.views import *

app_name = "phone"

urlpatterns = [
    path("ho/", index),
    path("ho/<int:my_id>/", indexItem, name="detail"),

]
