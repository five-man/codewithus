from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from solve.models import Algorithm, Likes, Solution, Comment
from member.models import Member
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages


# def algo(request): # 파라미터 필요
#     x = dt.datetime.now()
#     today = x.day
#     algo_date_dict = Algorithm.objects.filter(algo_update__day=today)
#     result = ''
#     result = ['%s %s %s<br>' % (i.algo_title, i.algo_update, i.algo_detail) for i in algo_date_dict]
#     #render (request, 'solve/show.html', algo_date_dict)
#     return HttpResponse(result)

# # Create your views here.
# def print_today(request):
#     #x = dt.datetime.now()
#     today = 25
#     algo = Algorithm.objects.filter(algo_update__day=today)
#     #algo = Algorithm.objects.all() 
#     return render(request, 'solve/show.html', {'info':algo})

def problem_list(request):
    m = Member.objects.all()

    now_page = request.GET.get('page', 1)
    now_page = int(now_page)

    #algo_list = Algorithm.objects.order_by('-algo_update')
    #algo_list = Algorithm.objects.select_related('blog').get(id=5)
    #a = Algorithm.objects.all()
#     algo = Algorithm.objects.first()
#     name = Member.objects.filter(member_name=algo)

#     order_qs = OrderLog.objects.values(
#     'created', 'product__name', 'product__price'
# )   
    algo_list = Algorithm.objects.values(
                                        'algo_no','algo_update', 'algo_title', 'algo_detail', 
                                        'member_no__member_name', 'tag_id__tag_name').order_by('-algo_update')
    #sol_list = Algorithm.objects.values('algo_no', 'algo_no__sol_no')

    
    #algo_list = Algorithm.objects.order_by('-algo_no')

    p = Paginator(algo_list, 5)
    page_obj = p.get_page(now_page)

    start_page = (now_page-1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages

    context = {'algo_list' : page_obj,
                'page_range' : range(start_page, end_page+1)}


    # page = request.GET.get('page',1)
    # page = int(page)

    # member_list = Member.objects.order_by('-member_no')

    # p = Paginator(member_list, 10)
    # page_obj = p.get_page(page)

    # start_page = (page - 1) // 10 * 10 + 1
    # end_page = start_page + 9
    # if end_page > p.num_pages:
    #     end_page = p.num_pages

    # context = {'member_list':page_obj,
    #             'page_range' : range(start_page, end_page +1)}

    return render(request,"solve/problem_list.html", context)


def exam(request, algo_no):
    algo = Algorithm.objects.get(algo_no=algo_no)
    return render(request, "solve/exam.html", {'algo':algo})

# def sol_print(sol_no):
#     cmt_detail = []
#     cmt_mem = []
#     like_count = []
#     cmt_detail.append(Comment.objects.filter(sol_no__in=value).values('comment_detail'))
#     cmt_mem.append(Comment.objects.filter(sol_no__in=value).values('member_no__member_name'))
#     like_count.append(Likes.objects.filter(sol_no__in=value).count())
#     sol_no = Solution.objects.filter(algo_no=algo_no).values_list('sol_no', flat=True) #'cmt_rel_sol_no'

def sol_list(request, algo_no):
    # sol = Solution.objects.filter(algo_no=algo_no).values('sol_no', 'sol_detail', 'member_no__member_name')
    # sol_no = Solution.objects.filter(algo_no=algo_no).values_list('sol_no', flat=True) #'cmt_rel_sol_no'
    # # sol_no =1
    # like_count = []
    #socm = Solution.objects.prefetch_related('cmt_rel_sol_no').prefetch_related('likes_rel_sol_no').filter(algo_no=algo_no).values('sol_no', 'sol_detail', 'member_no__member_name', 'cmt_rel_sol_no__comment_detail','cmt_rel_sol_no__member_no__member_name', 'likes_rel_sol_no__likes_no')
    socm = Solution.objects.prefetch_related('cmt_rel_sol_no')
    socm = socm.prefetch_related('likes_rel_sol_no')
    socm = socm.filter(algo_no=algo_no)
    # socm = socm.values('sol_no', 'sol_detail', 'member_no__member_name', 'cmt_rel_sol_no__comment_detail','cmt_rel_sol_no__member_no__member_name', Count('likes_rel_sol_no__likes_no'))
    
    
    # like_count.append(Likes.objects.filter(sol_no__in=socm.sol_no).count())
    socm = socm.values('sol_no', 'sol_detail', 'member_no__member_name', 'cmt_rel_sol_no__comment_detail','cmt_rel_sol_no__member_no__member_name', 'likes_rel_sol_no__likes_no').annotate(count=Count('likes_rel_sol_no__likes_no'))
    # socm2 = socm.filter(likes_rel_sol_no='likes_rel_sol_no').count()
    # cmt = Comment.objects.filter(sol_no=sol_no)
    # solcmt = sol_no.union(cmt, all=True)

    # #solcmt = Solution.objects.select_related('algo_no', ).select_related('likes', 'algo_no')
    # solcmt = Solution.objects.select_related('sol_no', 'comment_detail')


    #solcmlike = Likes.objects.select_related(solcm)
    # cmt_detail = Comment.objects.filter(sol_no__in=sol_no).values('comment_detail')
    # cmt_mem = Comment.objects.filter(sol_no__in=sol_no).values('member_no__member_name')
    # like = Likes.objects.filter(sol_no__in=sol_no)
    # cmt = []
    # cmt = Comment.objects.filter(sol_no__in=sol_no).values('comment_detail')
    # like_count=Likes.objects.filter(sol_no__in=sol_no).count()
    #sol_no=1
    # con = sol.union(cmt_detail, cmt_mem, like, all=True)
    # cmt_detail = []
    # # cmt_mem = []
    # like_count = []
    # sols = []
    # for person in person_set:
    # print(person.last_name)
    # for i in sol_no:
        # sols.append(i)
    # for i in sol_no():
    #     sol = []
    #     sol.append(i)
    # for value in range(len(sol_no)):
    #     cmt_detail = Comment.objects.filter(sol_no=value).values('comment_detail')
    #     cmt_mem = Comment.objects.filter(sol_no=value).values('member_no__member_name')
        # like_count = Likes.objects.filter(sol_no=sol_no[value]).count()
        # con = sol.union(cmt_detail, cmt_mem, like_count, all=True)
    
    #comment = Comment.objects.values('comment_detail')
    return render(
        request, 'solve/solutions.html',
        {'socm':socm,
        # 'cmt_detail':cmt_detail,
        # 'cmt_mem':cmt_mem,
        # 'like_count':like_count,
        # 'con':con
        }
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
