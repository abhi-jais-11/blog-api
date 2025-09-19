
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import *

router = DefaultRouter()
router.register(r'posts', PostReadOnlyViewSet, basename='post')
router.register(r'category', CategoryReadOnlyViewSet, basename='category')
router.register(r'tags', TagReadOnlyViewSet, basename='tags')
urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)