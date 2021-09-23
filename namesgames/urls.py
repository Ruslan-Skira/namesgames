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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from employees.views import AdminEmployeeViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="namesgames API",
        default_version="v1",
        description="Welcome to learning namesgames",
        terms_of_service="https://www.namesgames.org",
        contact=openapi.Contact(email="contact@namesgames.org"),
        license=openapi.License(name="namesgmames IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

urlpatterns = [
    re_path(
        r"^doc(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "doc/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("api/v1/companies/", include("company.urls")),
    path("api/v1/employees/", include("employees.urls")),
    path("accounts/", include("allauth.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("me/", include("accounts.urls")),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetView.as_view(), name="password_reset"),
]

router.register(r"api/v1/admin/employees", AdminEmployeeViewSet, basename='employees')

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path("__debug__/", include(debug_toolbar.urls)),
                  ] + urlpatterns
urlpatterns += router.urls
