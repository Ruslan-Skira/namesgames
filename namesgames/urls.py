"""namesgames URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
    how it could be????
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from company.views import CompanyViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="namesgames API",
        default_version='v1',
        description="Welcome to learning namesgames",
        terms_of_service="https://www.namesgames.org",
        contact=openapi.Contact(email="contact@namesgames.org"),
        license=openapi.License(name="namesgmames IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)


urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  # <-- Here
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  # <-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  # <-- Here
    path('', include(router.urls)),
    path('linkedin_find/', include('scraping.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/v1/', include('company.urls')),
    # path(r'^api/', include(router.urls)),
    path('api/', include((router.urls, 'company'), namespace='api')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
urlpatterns += router.urls
