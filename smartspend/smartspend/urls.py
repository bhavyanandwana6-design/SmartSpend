from django.contrib import admin
from django.urls import path
from expenses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('add/', views.add_expense, name='add_expense'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('ai-summary/', views.ai_summary, name='ai_summary'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
]