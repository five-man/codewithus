from django.urls import path
from . import views

app_name = 'solve'

urlpatterns = [
    path('problem_list/', views.problem_list, name='problem_list'),    
    path('problem_upload/', views.problem_upload, name='problem_upload'),    
    #path('today_exam/', views.today_exam, name='today_exam'),   
    #path('exam<int:algo_no>/', views.exam, name='exam'),
    #path('solutions<int:algo_no>/', views.solutions, name='solutions'),
    #path('solutions<int:algo_no>/', views.solutions, name='solutions'),
    #path('update_exam<int:algo_no><int:sol_no>/', views.update_exam, name='update_exam'),
    #path('algo/', views.algo, name = 'algo'),
    #path('print/', views.print_today),
    path('problem_list/exam<int:algo_no>/', views.exam, name='exam'),
    path('problem_upload/complete', views.problem_upload_complete, name='problem_upload_complete'),    
    # path('problem_upload/fail', views.problem_upload_fail, name='problem_upload_fail'),    
    path('today_exam/', views.today_exam, name='today_exam'),    
    path('problem_list/solutions<int:algo_no>/', views.solutions, name='solutions'),
    path('solutions/', views.solutions, name='solutions'),    
    path('reply/', views.reply, name='reply'),    
]