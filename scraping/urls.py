from django.urls import path

from .views import LinkedInFindView

urlpatterns = [
    path('', LinkedInFindView.as_view(), name='home'),
]
