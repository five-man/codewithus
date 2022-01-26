from django.shortcuts import redirect, render
from .models import Member
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def main(request):
    if request.method == "POST":

        return render(request,"solve/today_exam.html")
    else:
        return render(request,"member/main.html")

def login(request):
    if request.method == 'POST':
        member_email = request.POST.get('member_email')
        member_password = request.POST.get('member_password')
        try:
            m = Member.objects.get(member_email=member_email, member_password=member_password)
        except Member.DoesNotExist as e:
            messages.info(request, '아이디 혹은 비밀번호를 확인해주세요.')
            return render(request, 'member/login.html')
        else:
            request.session['member_no'] = m.member_no
            request.session['member_email'] = m.member_email
            request.session['member_name'] = m.member_name
        return redirect('/main/')
    else:
        return render(request, 'member/login.html')


def signup(request):
    if request.method == 'POST':
        member_email = request.POST.get('member_email')
        member_password = request.POST.get('member_password')
        member_name = request.POST.get('member_name')
        
        m = Member(
            member_email=member_email, 
            member_password=member_password, 
            member_name=member_name)
        m.member_joindate = timezone.now()
        m.save()

        return redirect('/login/')
    else:
        return render(request, 'member/signup.html')

def logout(request):
    
    request.session.flush() # 전체 삭제
    return redirect('/main/')