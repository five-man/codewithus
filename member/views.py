from django.shortcuts import render
from .models import Member
from django.utils import timezone
from django.http import HttpResponse

# Create your views here.
def main(request):

    return render(request,"member/main.html")

def login(request):

    return render(request,"member/login.html")

def signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')
        user_name = request.POST.get('user_name')
        
        m = Member(
            user_id=user_id, user_pw=user_pw, user_name=user_name)
        m.date_joined = timezone.now()
        m.save()

        return HttpResponse(
            '가입 완료<br>%s %s %s' % (user_id, user_pw, user_name))
    else:
        return render(request, 'member/signup.html')
