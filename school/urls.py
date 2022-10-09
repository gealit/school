from django.contrib import admin
from django.urls import path
from django.conf import settings

admin.site.site_header = f"Администрирование {settings.COMPANY}"
admin.site.site_title = f"Администрирование {settings.COMPANY}"
admin.site.index_title = f"Добро пожаловать на сервис {settings.COMPANY}"

urlpatterns = [
    path('admin/', admin.site.urls),
]
