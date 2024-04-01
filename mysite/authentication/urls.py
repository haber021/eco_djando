from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'authentication'


urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('registers/', views.RegisterView.as_view(), name='registers'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('validate-username', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()), name='validate_email'),
    path('activate/<uidb64>/<token>/', views.VerificationView.as_view(), name='activate'),
    path('request-password/', views.ResetPassword.as_view(), name='request-password'),
    path('set-new-password/<uidb64>/<token>/', views.CompletePasswordReset.as_view(), name='reset-user-password'),
]