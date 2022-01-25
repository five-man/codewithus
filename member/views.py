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
        member_email = request.POST.get('member_email')
        member_password = request.POST.get('member_password')
        member_name = request.POST.get('member_name')
        
        m = Member(
            member_email=member_email, member_password=member_password, member_name=member_name)
        m.member_joindate = timezone.now()
        m.save()

        return HttpResponse(
            '가입 완료<br>%s %s %s' % (member_email, member_password, member_name))
    else:
        return render(request, 'member/signup.html')
