from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from distribution.urls import router as distribution_router
from distribution.urls import urlpatterns as distribution_urls

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(distribution_router.urls)),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    path('admin/', admin.site.urls),
]

urlpatterns += distribution_urls