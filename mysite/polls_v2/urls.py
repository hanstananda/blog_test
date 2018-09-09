from django.urls import path

from . import views

app_name = 'polls_v2'

"""
urlpatterns = [
    # ex: /polls_v2/
    path('', views.index, name='index'),
    # ex: /polls_v2/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # added the word 'specifics'
    path('specifics/<int:question_id>/', views.detail, name='detail'),
    # ex: /polls_v2/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls_v2/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]"""

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

# NOTE! pk here means primary key!! It searches on primary key!