
from django.contrib import admin
from django.urls import path

from billing import views
urlpatterns = [
    path('', views.home, name='home'),
    path('Profile', views.Profile, name="Profile"),
    path('RegisterShop/', views.RegisterShop.as_view(), name='RegisterShop'),
    path('CreateBill/', views.CreateBill.as_view(), name='CreateBill'),
    path('AddItems', views.AddItems.as_view(), name='AddItems'),
    path('NewBill/', views.NewBill, name='NewBill'),
    path('ComplateDelete/', views.ComplateDelete, name='ComplateDelete'),
    path('DeleteItem/', views.DeleteItem, name='DeleteItem'),
    path('billinfo/', views.billinfo, name='billinfo'),
    path('GetBill/', views.GetBill.as_view(), name='GetBill'),
    path('ShowBill/', views.ShowBill, name='ShowBill'),
    path('EditShopDetails/', views.EditShopDetails, name='EditShopDetails'),

   
   
]
