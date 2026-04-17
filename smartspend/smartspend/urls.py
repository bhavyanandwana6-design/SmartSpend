from django.contrib import admin
from django.urls import path
from expenses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('add/', views.add_expense, name='add_expense'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
]