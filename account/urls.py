
from django.urls import path
from account import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
    path('Registration/', views.register, name='Registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('ChangePassword/',views.ChangePasswordView , name = 'ChangePassword' ),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
   
]
