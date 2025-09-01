from django.urls import path
from .views import UsersView


urlpatterns = [
    path('signup', UsersView.as_view(), name='auth'),
]