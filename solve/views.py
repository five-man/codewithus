from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from solve.models import Algorithm, Likes, Solution, Comment
from member.models import Member
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages

def problem_list(request):
    m = Member.objects.all()

    now_page = request.GET.get('page', 1)
    now_page = int(now_page)
  
    algo_list = Algorithm.objects.values(
                                        'algo_no','algo_update', 'algo_title', 'algo_detail', 
                                        'member_no__member_name', 'tag_id__tag_name').order_by('-algo_update')
    p = Paginator(algo_list, 5)
    page_obj = p.get_page(now_page)

    start_page = (now_page-1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages

    context = {'algo_list' : page_obj,
                'page_range' : range(start_page, end_page+1)}


    return render(request,"solve/problem_list.html", context)


def exam(request, algo_no):
    algo = Algorithm.objects.get(algo_no=algo_no)
    return render(request, "solve/exam.html", {'algo':algo})


def sol_list(request, algo_no):
    socm = Solution.objects.prefetch_related('cmt_rel_sol_no')
    socm = socm.prefetch_related('likes_rel_sol_no')
    socm = socm.filter(algo_no=algo_no)
    
    
    socm = socm.values('sol_no', 'sol_detail', 'member_no__member_name', 'cmt_rel_sol_no__comment_detail','cmt_rel_sol_no__member_no__member_name', 'likes_rel_sol_no__likes_no').annotate(count=Count('likes_rel_sol_no__likes_no'))
    
    return render(
        request, 'solve/solutions.html',
        {'socm':socm,}
    )
#@login_required(login_url='member:login')
def update_exam(request, sol_no):
    sol = Solution.objects.get(sol_no=sol_no)
    if request.method == 'POST':
        sol.sol_detail = request.POST('contents')
        sol.member_no = request.POST('member_no')
        sol.algo_no = request.POST('algo_no')
        sol.save()
    else:
        sol = sol()
        return render(request, 'solve/update_exam.html', {sol:'sol'})

    # member_no = request.session.get('member_no')
    # if member_no != pk:
    #     messages.error(request, '수정 권한이 없습니다')
    #     return redirect('원래 페이지로 가기')

    # else:
    #     return redirect('edit_exam.html')
    


def delete_exam(request, pk):
    sol = Solution.objects.get(sol_no=pk)
    sol.delete()
    return redirect('원래 페이지')

def problem_upload(request):
    
    #
    #   오늘의 문제가 있다면 업로드 못하게 막는 로직
    #
    if request.method == 'POST':
        algo_title = request.POST.get('subject')
        algo_detail = request.POST.get('contents')
        #member_no = request.session['member_no']
        member_no = request.session.get('member_no')
        #member_name = request.session.get('member_name')
        #now = timezone.localtime()
        
        
        a = Algorithm(
            algo_title=algo_title, algo_detail=algo_detail, tag_id=1,
            member_no=Member.objects.get(member_no=member_no))
        a.algo_update = timezone.now()
        a.save()
        request.session['algo_no'] = a.algo_no

        # 글이 써지면 오늘의 문제로 
        return redirect('/today_exam/')
    else:
        # 
        return render(request, 'solve/problem_upload.html')

    # return render(request,"solve/problem_upload.html")

def today_exam(request):
    if request.method=="POST":
        sol_detail = request.POST.get('contents')
        member_no = request.session.get('member_no')
        algo_no = request.session.get('algo_no')

        s = Solution(
            sol_detail = sol_detail,
            algo_no = Algorithm.objects.get(algo_no=algo_no),
            sol_like = 0,
            member_no=Member.objects.get(member_no=member_no)
        )
        s.save()
        return redirect('solve/solutions.html')
    else:
        return render(request,"solve/today_exam.html")

def exam(request, algo_no):
    algo = Algorithm.objects.get(algo_no=algo_no)
    return render(request, "solve/exam.html", {'algo':algo})

def push_likes(request):
    pass

def on_comment(request):
    pass
