from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.views import api_endpoints

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('apps/', include('apps.urls')),
    path('', api_endpoints, name='api_endpoint'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
