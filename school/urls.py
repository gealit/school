from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from accounts.views import LoginPage

admin.site.site_header = f"Администрирование {settings.COMPANY}"
admin.site.site_title = f"Администрирование {settings.COMPANY}"
admin.site.index_title = f"Добро пожаловать на сервис {settings.COMPANY}"

urlpatterns = [
    path('', include('board.urls', namespace='board')),
    path('user/', include('accounts.urls', namespace='account')),
    path('admin/', admin.site.urls),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
