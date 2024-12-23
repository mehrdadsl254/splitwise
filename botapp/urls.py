from django.urls import path
from botapp import views
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/<str:group_id>/', views.group_detail, name='group_detail'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('create_group/', views.create_group, name='create_group'),
    path('search_users/', views.search_users, name='search_users'),
    path('add_user_to_group/<str:group_id>/<str:user_id>/', views.add_user_to_group, name='add_user_to_group'),
    path('webhook/', views.webhook_handler, name='webhook_handler'),
    path('webapp/', views.webapp, name='webapp'),
]