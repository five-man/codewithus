from django.urls import path
from . import views

app_name = 'solve'

urlpatterns = [
    path('todaysol/', views.today_solutions, name='todaysol'),  
    path('problem_list/', views.problem_list, name='problem_list'),    
    path('problem_upload/', views.problem_upload, name='problem_upload'),    
    path('today_exam/', views.today_exam, name='today_exam'),
    path('today_reply/', views.today_reply, name='today_reply'),    
    path('reply/', views.reply, name='reply'),    
    path('sol_del/', views.sol_del, name='sol_del'),    

    #path('exam<int:algo_no>/', views.exam, name='exam'),
    #path('solutions<int:algo_no>/', views.solutions, name='solutions'),
    #path('solutions<int:algo_no>/', views.solutions, name='solutions'),
    #path('update_exam<int:algo_no><int:sol_no>/', views.update_exam, name='update_exam'),
    #path('algo/', views.algo, name = 'algo'),
    #path('print/', views.print_today),
    #path('problem_list/exam<int:algo_no>/', views.exam, name='exam'),
    path('problem_upload/complete', views.problem_upload_complete, name='problem_upload_complete'),    
    # path('problem_upload/fail', views.problem_upload_fail, name='problem_upload_fail'),    
      
    path('exam<int:in_algo_no>/', views.exam, name='exam'),
    path('exam<int:in_algo_no>/solutions/', views.solutions, name='solutions'),
    #path('exam<int:algo_no>/solve/solutions/', views.solutions, name='solget'),
    path('update_exam<int:algo_no><int:sol_no>/', views.update_exam, name='update_exam'),

    path('exam<int:algo_no>/solutions', views.exam, name='ex_solution'),
    # path('solutions/', views.solutions, name='solutions'),    
    
]