from django.urls import include, re_path, path
from .views import UserRegistrationView, UsersListView, GetNewsletterView

# urlpatterns = [
#     path('login/', UserLoginView.as_view(), name='login'),
# ]
# urlpatterns = [
#     re_path(r'^newsletter/', GetNewsletterView.as_view(), name='newsletter'),
#     re_path(r'^registration/', UserRegistrationView.as_view(), name='registration'),
#     re_path(r'^users_list/$', UsersListView.as_view(), name='users-list'),
# ]
