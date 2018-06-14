from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'tracker'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.UpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]