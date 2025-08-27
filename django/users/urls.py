from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    # Combines GET, PUT, DELETE for a specific user
    path('user/<int:user_id>/', views.user_detail_view, name='user-detail'),
    path('user/<int:user_id>/update', views.user_detail_view, name='user-update-delete'), 
]