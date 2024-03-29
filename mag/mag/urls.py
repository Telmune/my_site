from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('phone/', include('phone.urls', namespace="phone")),
    path('users/', include('users.urls', namespace="users"))

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)