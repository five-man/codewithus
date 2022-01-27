import datetime
import json
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from numpy import save
import os
from config.settings import BASE_DIR, MEDIA_ROOT, STATIC_ROOT
from solve.models import Algorithm,AlgorithmImage, Comment, Solution, Tag
from member.models import Member
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.
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

def problem_upload(request):
    # now = datetime.datetime.now()
    # nowDate = now.strftime('%Y-%m-%d')  
        
    if request.method == 'POST':
        algo_title = request.POST.get('subject')
        algo_detail = request.POST.get('contents')
        tag = request.POST.get('algorithm_tag')
        member_no = request.session.get('member_no')
        uploadedFile= request.FILES.getlist("image")
        
        #
      
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        
        try:
            is_ok = Algorithm.objects.get(algo_update=nowDate)
        except Algorithm.DoesNotExist as e:
            a = Algorithm(
                algo_title=algo_title, 
                algo_detail=algo_detailaa, 
                member_no=Member.objects.get(member_no=member_no),
                tag_id=tag,
                algo_update = nowDate
            )
            a.save()
            for uploadFile in uploadedFile:
                # image_name = 
                i = AlgorithmImage(
                    image_name=uploadFile.name,
                    image_root= "static/media/",
                    algo_no=Algorithm.objects.get(algo_update=nowDate))
                i.save()
                save_path = os.path.join(STATIC_ROOT,i.image_name)
                with open(save_path, 'wb') as file:
                    for chunk in uploadFile.chunks():
                        file.write(chunk)
                
            # 글이 써지면 오늘의 문제로 
            return render(request, 'solve/problem_upload_complete.html')
        
        return render(request, 'solve/problem_upload_fail.html')
    else:
        # 
        return render(request, 'solve/problem_upload.html')

    # return render(request,"solve/problem_upload.html")

       
    

def today_exam(request):
    if request.method=="POST":
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        sol_detail = request.POST.get('contents')
        member_no = request.session.get('member_no')
        membername = Member.objects.get(member_no = member_no)
        algo_no = Algorithm.objects.get(algo_update = nowDate)

        s = Solution(
            sol_detail = sol_detail,
            algo_no = Algorithm.objects.get(algo_no=algo_no.algo_no),
            sol_like = 0,
            member_no=Member.objects.get(member_no=member_no)
        )
        
        context = {
            'today_sols' : Solution.objects.filter(algo_update=nowDate),
            'name' : membername.member_name
        }
        
        s.save()
        return render(request, 'solve/solutions.html', context)
    else:
        # return render(request,"solve/today_exam.html")
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        
        today_algo = Algorithm.objects.get(algo_update = nowDate)
        algo_image_object = AlgorithmImage.objects.filter(algo_no= today_algo)
        # algo_image_object.
        # print(today_algo)
        
        
        return render(request, 'solve/today_exam.html', {'image':algo_image_object})


# if __name__ =="__main__":
#     problem_upload(request)

def problem_upload_complete(request):
    
    # now = datetime.datetime.now()
    # nowDate = now.strftime('%Y-%m-%d')
    
    # today_algo = Algorithm.objects.get(algo_no = 87)
    # algo_image_object = AlgorithmImage.objects.filter(algo_no=today_algo)

    
    # return render(request, 'solve/today_exam.html', {'image':algo_image_object.image_name})

    return redirect("/main/")



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
=======
    
    
    
    
    return render(request,"solve/today_exam.html")

def solutions(request,sol_no=50):
    solution = Solution.objects.get(sol_no=sol_no)

    reply = Comment.objects.filter(sol_no=sol_no)

    try:
        session = request.session.get('member_no')
        context = {
            'solution': solution,
            'reply': reply,
            'session': session,
        }
        return render(request, 'solve/solutions.html', context)
    except KeyError:
        return redirect('member/main')


def reply(request):
    member_no = request.session.get('member_no')
    jsonObject = json.loads(request.body)

    reply = Comment.objects.create(
        sol_no=Solution.objects.get(sol_no=50),
        algo_no=Solution.objects.get(algo_no=50),
        member_no=Member.objects.get(member_no=member_no),
        comment_detail=jsonObject.get('comment_detail'),
    )
    reply.save()

    context = {
        # 'name' : reply.member_no,
        'content' : reply.comment_detail,
    }

    return JsonResponse(context)