from django.urls import path
from . import views

app_name = 'solve'

urlpatterns = [
    path('problem_list/', views.problem_list, name='problem_list'),    
    path('problem_upload/', views.problem_upload, name='problem_upload'),    
    path('problem_upload/complete', views.problem_upload_complete, name='problem_upload_complete'),    
    # path('problem_upload/fail', views.problem_upload_fail, name='problem_upload_fail'),    
    path('today_exam/', views.today_exam, name='today_exam'),    
    path('solutions/', views.solutions, name='solutions'),    
]