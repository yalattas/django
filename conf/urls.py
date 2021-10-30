"""ecs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings

# To include current API version in the URL
api = f'api/{settings.API_VERSION}'

# for swagger documentation
# schema_view = get_swagger_view(title='Pastebin API')
schema_view = get_schema_view(
    openapi.Info(
        title="application API",
        default_version="v1",
        description="Here is a brief about the application",
        terms_of_service="https://example.com/privacy-policy.html",
        contact=openapi.Contact(email="username@domain.com"),
        license=openapi.License(name="Commercial"),
    ),
    public=False,
    # to restrict access to admin only
    permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('health_check.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    path('', include('apps.main.urls')),
    path(f'{api}/points/', include('apps.points.urls')),
]
