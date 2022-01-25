from datetime import timezone
from django.http import HttpResponse
from django.shortcuts import render

from solve.models import Algorithm

# Create your views here.
def problem_list(request):

    return render(request,"solve/problem_list.html")

def problem_upload(request):
    if request.method == 'POST':
        algo_title = request.POST.get('subject')
        algo_detail = request.POST.get('contents')
        member_name = request.session.member_name
        
        a = Algorithm(
            algo_title=algo_title, algo_detail=algo_detail, member_name=member_name)
        a.algo_update = timezone.now()
        a.save()

        # 글이 써지면 오늘의 문제로 
        return HttpResponse(
            '가입 완료<br>%s %s %s' % (algo_title, algo_detail, member_name))
    else:
        # 
        return render(request, 'solve/problem_upload.html')

    # return render(request,"solve/problem_upload.html")

def today_exam(request):

    return render(request,"solve/today_exam.html")