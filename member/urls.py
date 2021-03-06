from django.urls import path
from . import views

app_name = 'member'

urlpatterns = [
    path('signup/', views.signup, name='signup'),    
    path('main/', views.main, name='main'),    
    path('login/', views.login, name='login'),    
    path('logout/', views.logout, name='logout'),   
    # path('activate/<str:uidb64>/<str:token>', views.Activate.as_view(), name='status'), 
]