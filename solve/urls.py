from django.urls import path
from . import views

app_name = 'solve'

urlpatterns = [
    path('problem_list/', views.problem_list, name='problem_list'),    
    path('problem_upload/', views.problem_upload, name='problem_upload'),    
    path('today_exam/', views.today_exam, name='today_exam'),   
    path('today_exam<int:algo_no>/', views.today_exam, name='today_exam2'),
    path('problem_list/exam<int:algo_no>/', views.exam, name='exam'),
    path('problem_list/sol_list<int:algo_no>/', views.sol_list, name='sol_list'),
    path('today_exam/update_exam<int:sol_no>/', views.update_exam, name='update_exam')
    #path('algo/', views.algo, name = 'algo'),
    #path('print/', views.print_today),
]