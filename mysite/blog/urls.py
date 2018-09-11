from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.CategoryPostList.as_view(), name='category'),
    path('login/', views.login, name='login'),
    path('success/', views.success, name="success"),
    path('fail/', views.fail, name="fail"),
]
