from django.contrib import admin  
from django.conf.urls import url
from django.urls import path
from .views import ListUsersView, UserDetailView , ListCsvUsersView
urlpatterns = [  

    path('/<int:pk>', UserDetailView.as_view(), name="user-detail"),
    path('/all/csv', ListCsvUsersView.as_view(), name="users-csv"),
    path('/', ListUsersView.as_view(), name="users"),

    
] 