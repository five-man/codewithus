from django.urls import path
from . import views

app_name = 'solve'

urlpatterns = [
    path('problem_list/', views.problem_list, name='problem_list'),    
    path('problem_upload/', views.problem_upload, name='problem_upload'),    
    path('today_exam/', views.today_exam, name='today_exam'),    
    path('solutions/', views.solutions, name='solutions'),    
    path('reply/', views.reply, name='reply'),    
]