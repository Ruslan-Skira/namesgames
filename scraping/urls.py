from django.urls import path, include

from .views import LinkedInFindView

urlpatterns = [
    path('', LinkedInFindView.as_view(), name='home'),
    ]
