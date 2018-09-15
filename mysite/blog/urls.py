from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<int:pk>/', views.CategoryPostList.as_view(), name='category'),
    path('post/<int:pk>/', views.PostView.as_view(), name='post'),
    path('login/', views.login_view, name='login_view'),
    path('success/', views.success, name="success"),
    path('fail/', views.fail, name="fail"),
    path('logout/', views.logout_view, name='logout_view'),
    path('unlike/', views.unlike, name='unlike_view'),
    path('like/', views.like, name='like_view'),
    path('add_comment/', views.add_comment, name='add_comment_view'),
]
