from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    # Frontend
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
    # Backend
    path('admin/', views.admin_view, name='admin-site'),
    # Categories GET
    path('admin/categories/', views.CategoriesAdminView.as_view(), name='CategoriesAdminView'),
    path('admin/categories/create', views.CategoriesAdminCreate.as_view(), name='CategoriesAdminCreate'),
    path('admin/categories/edit/<int:pk>', views.CategoriesAdminEdit.as_view(), name='CategoriesAdminEdit'),
    # Categories POST
    path('admin/categories/add_category', views.add_category, name='add_category'),
    path('admin/categories/delete_category', views.delete_category, name='delete_category'),
    path('admin/categories/edit_category', views.edit_category, name='edit_category'),
    # Users GET
    path('admin/users/', views.UsersAdminView.as_view(), name='UsersAdminView'),
    # Users POST
    path('admin/users/ban', views.ban_user, name='ban_user'),
    path('admin/users/unban', views.unban_user, name='unban_user'),
    # Posts GET
    path('admin/posts/', views.PostsAdminView.as_view(), name='PostsAdminView'),
    path('admin/posts/<int:pk>', views.PostsAdminView.as_view(), name='DetailPostAdminView'),
    path('admin/posts/create', views.PostsAdminCreate.as_view(), name='PostsAdminCreate'),
    path('admin/posts/edit/<int:pk>', views.PostsAdminEdit.as_view(), name='PostsAdminEdit'),
    # Posts POST
    path('admin/posts/add_post', views.add_post, name='add_post'),
    path('admin/posts/delete_post', views.delete_category, name='delete_post'),
    path('admin/posts/edit_post', views.edit_category, name='edit_post'),
]
