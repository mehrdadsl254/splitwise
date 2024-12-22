from django.urls import path
from botapp import views

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

]