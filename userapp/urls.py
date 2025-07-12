from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout_user'),
    path('question_detail/<int:question_id>/', views.question_detail, name='question_detail'),
    path('ask_question/', views.ask_question, name='ask_question'),


]
