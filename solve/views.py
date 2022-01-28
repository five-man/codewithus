from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from matplotlib.style import context
from numpy import save
import datetime, json, os
from config.settings import BASE_DIR, MEDIA_ROOT, STATIC_ROOT
from solve.models import Algorithm, AlgorithmImage, Comment, Solution, Tag, Likes
from member.models import Member
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
from django.urls import reverse
import json

# Create your views here.

def ceil(n):
    if n ==int(n):
        return n
    else:
        return int(n)+1

def problem_list(request):
    now_page = request.GET.get('page', 1)
    now_page = int(now_page)
    algo_list = Algorithm.objects.values(
                                        'algo_no','algo_update', 'algo_title', 'algo_detail', 
                                        'member_no__member_name', 'tag_id__tag_name').order_by('-algo_no')
    p = Paginator(algo_list, 5)
    page_obj = p.get_page(now_page)

    start_page = (now_page-1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages
    context = {'algo_list' : page_obj,
                'page_range' : range(start_page, end_page+1)}
    # request.session['algo_no'] = algo_list.algo_no

    return render(request,"solve/problem_list.html", context)


def exam(request, algo_no):
    al = algo_no
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    today_algo = Algorithm.objects.get(algo_no = algo_no)
    total_member = Member.objects.count()
    today_member = Solution.objects.filter(algo_no = today_algo).count()
    percent= ceil(today_member/total_member*100)
    
    if request.method=="POST":
        sol_detail = request.POST.get('contents')
        member_no = request.session.get('member_no')
        algo_no = Algorithm.objects.get(algo_no=algo_no)

        s = Solution(
            sol_detail = sol_detail,
            algo_no = algo_no,
            sol_like = 0,
            member_no=Member.objects.get(member_no=member_no)
        )
        s.save()
        return redirect('solutions'+str(al)+'/')
    else:
        algo_image_object = AlgorithmImage.objects.filter(algo_no= today_algo)
        pe=str(percent) +"%"
        data = {
                'percent': percent,
                'image': algo_image_object,
                'pe':pe,
                'algo_no': algo_no
                }
        return render(request,"solve/exam.html", data)



def solutions(request, sol_no=2):
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

    # if request.method == 'POST':
    #     print('its post')
    #     try:
    #         is_ok = Solution.objects.get(member_no = request.session.get('member_no'))
    #         print('************************************************')
    #     except Solution.DoesNotExist as e: 
    #         sol_detail = request.POST.get('contents')
    #         member_no = request.session.get('member_no')
    #         # membername = Member.objects.get(member_no = member_no)
    #         algo_no = Algorithm.objects.get(algo_no = algo_no)

    #         s = Solution(
    #             algo_no = algo_no,
    #             sol_detail = sol_detail,
    #             sol_like = 0,
    #             member_no=Member.objects.get(member_no=member_no)
    #         )
            
            
    #         # today_sols = Solution.objects.filter(algo_update=nowDate)
    #         s.save()
            
    #         # 문제 제출 확인
    #         return render(request, 'solve/solution_insert.html')
    #     return render(request, 'solve/already_sol.html')
    # else:
        
    #     solution = Solution.objects.filter(algo_no__in=algo_no)
    #     reply = Comment.objects.get(Solution=solution)


    #     try:
    #         session = request.session.get('member_no')
    #         context = {
    #             'solution': solution,
    #             'reply': reply,
    #             'session': session,
    #         }
    #         return render(request, 'solve/solutions.html', context)
    #     except KeyError:
    #         return redirect('member/main')    
        
#@login_required(login_url='member:login')
def update_exam(request, sol_no, algo_no):
    sol = Solution.objects.get(sol_no=sol_no)
    #algo_no = sol.values('algo_no')
    if request.method == 'POST':
        sol.sol_detail = request.POST.get('contents')
        sol.save()
        return redirect('/solve/problem_list/sol_list'+str(algo_no)+'/')
    else:
        sol = Solution()
        return render(request, 'solve/update_exam.html', {'sol':sol})

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
                algo_detail=algo_detail, 
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
    
    if request.method=="POST": # 풀이 작성시
        try:
           is_ok = Solution.objects.get(member_no = request.session.get('member_no'))
        except Solution.DoesNotExist as e: 
            now = datetime.datetime.now()
            nowDate = now.strftime('%Y-%m-%d')
            
            sol_detail = request.POST.get('contents')
            member_no = request.session.get('member_no')
            # membername = Member.objects.get(member_no = member_no)
            algo_no = Algorithm.objects.get(algo_update = nowDate)

            s = Solution(
                algo_no = algo_no,
                sol_detail = sol_detail,
                sol_like = 0,
                member_no=Member.objects.get(member_no=member_no)
            )
            
            
            # today_sols = Solution.objects.filter(algo_update=nowDate)
            s.save()
            
            # 문제 제출 확인
            return render(request, 'solve/solution_insert.html')
        return render(request, 'solve/already_sol.html')
    else:
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        try:   
            # 진행상태바 퍼센트정보
            today_algo = Algorithm.objects.get(algo_update = nowDate)
            total_member = Member.objects.count()
            today_member = Solution.objects.filter(algo_no = today_algo).count()
            percent= ceil(today_member/total_member*100)
            # 이미지            
            algo_image_object = AlgorithmImage.objects.filter(algo_no= today_algo)
            pe=str(percent) +"%"
            data = {
                'percent': percent,
                'image': algo_image_object,
                'pe':pe
                }
        
        except Algorithm.DoesNotExist as e:
            # 오늘의 문제 없음
            return render(request, 'solve/no_today_exam.html')
        
        
        return render(request, 'solve/today_exam.html', data)




def problem_upload_complete(request):
    

    
    # return render(request, 'solve/today_exam.html', {'image':algo_image_object.image_name})

    return redirect("/main/")



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
    
    return render(request,"solve/today_exam.html")

# def solutions(request,sol_no=50):
#     solution = Solution.objects.get(sol_no=sol_no)

#     reply = Comment.objects.filter(sol_no=sol_no)


#     try:
#         session = request.session.get('member_no')
#         context = {
#             'solution': solution,
#             'reply': reply,
#             'session': session,
#         }
#         return render(request, 'solve/solutions.html', context)
#     except KeyError:
#         return redirect('member/main')



    


def reply(request):
    member_no = request.session.get('member_no')
    jsonObject = json.loads(request.body)
    solno = jsonObject.get('sol_no')
    reply = Comment.objects.create(
        sol_no=Solution.objects.get(sol_no=solno),
        algo_no=Solution.objects.get(sol_no=solno),
        member_no=Member.objects.get(member_no=member_no),
        comment_detail=jsonObject.get('comment_detail'),
    )
    reply.save()
    membername = Member.objects.get(member_no = member_no)
    context = {
        # 'name': serializers.serialize("json", reply.member_no),
        'content': reply.comment_detail,
        'pp': membername.member_name    
    }

    return JsonResponse(context)