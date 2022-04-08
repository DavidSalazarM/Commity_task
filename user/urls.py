from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from user import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('user_detail/', views.UserDetail.as_view()),
    path('change_pasword/', views.ChangePasswordView.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)
