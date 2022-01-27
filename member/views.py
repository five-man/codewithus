from django.shortcuts import redirect, render
from .models import Member
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def main(request):

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
        
        if Member.objects.filter(member_email = member_email):
            messages.info(request, "이미 존재하는 email 입니다.")
            return render(request, 'member/signup.html')
        
        mail_subject = '이메일 인증 요청'
        message = render_to_string('member/smtp_email.html', {
            'member_name': member_name
                })
        to_email = member_email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
                
        
        
        
        m = Member(
            member_email=member_email, member_password=member_password, member_name=member_name)
        m.member_joindate = timezone.now()
        m.save()
        
        return redirect('/login/')
    else:
        return render(request, 'member/signup.html')

def logout(request):
    
    request.session.flush() # 전체 삭제
    return redirect('/main/')



def message(domain, uidb64, token): 
    return f"아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n회원가입 링크 : http://{domain}/account/activate/{uidb64}/{token}\n\n감사합니다."

