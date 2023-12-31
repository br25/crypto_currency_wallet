from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('crypto_app.urls')),
    path('auth/', include('crypto_auth.urls')),
]
