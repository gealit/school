from django.contrib import admin
from django.urls import path, include
from django.conf import settings

admin.site.site_header = f"Администрирование {settings.COMPANY}"
admin.site.site_title = f"Администрирование {settings.COMPANY}"
admin.site.index_title = f"Добро пожаловать на сервис {settings.COMPANY}"

urlpatterns = [
    path('user/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
