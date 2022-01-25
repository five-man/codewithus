from datetime import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render

from solve.models import Algorithm

# Create your views here.
def problem_list(request):

    return render(request,"solve/problem_list.html")

def problem_upload(request):
    
    #
    #   오늘의 문제가 있다면 업로드 못하게 막는 로직
    #
    
    if request.method == 'POST':
        algo_title = request.POST.get('subject')
        algo_detail = request.POST.get('contents')
        member_no = request.session['member_no']
        
        a = Algorithm(
            algo_title=algo_title, algo_detail=algo_detail, member_no=member_no)
        a.algo_update = timezone.now()
        a.save()

        # 글이 써지면 오늘의 문제로 
        return redirect('/today_exam/')
    else:
        # 
        return render(request, 'solve/problem_upload.html')

    # return render(request,"solve/problem_upload.html")

def today_exam(request):

    return render(request,"solve/today_exam.html")