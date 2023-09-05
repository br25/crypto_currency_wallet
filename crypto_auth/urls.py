from django.urls import path
from django.contrib.auth import views as auth_views
from crypto_app.views import auth_views as views

urlpatterns = [
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetAPIView.as_view(), name='password-reset'),

]