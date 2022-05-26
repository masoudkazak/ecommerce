from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('cv-masoud-admin/', admin.site.urls),
    path('', include('item.urls')),
    path('api/', include('api.urls')),
    path('', include('account.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', schema_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
