from django.urls import path
from . import views

app_name="polls"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.Detail.as_view(), name='detail'),
    path('stam/', views.stam, name='stam'),
    path('<int:question_id>/vote', views.Vote.as_view(), name='vote'),
    path('newq/', views.NewQuestion.as_view(),name="newquestion"),
    path('newc/', views.NewChoice.as_view(),name="newchoice"),  
    path('register/', views.register, name='register'),      
    path('login/', views.LogInUser.as_view(), name='login'),      
    path('logout/', views.logUserOut, name='logout'),      
    # path('q/', views.Q.as_view(), name="q"),
]