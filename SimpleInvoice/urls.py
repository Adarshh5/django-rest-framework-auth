
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('billing.urls')),
    path('captcha/', include('captcha.urls')),
    path("api/users/", include("user.urls")),
]
