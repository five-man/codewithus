import datetime
import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from config.settings import MEDIA_ROOT, STATIC_ROOT
from member.models import Member
from django.contrib import messages
from django.core.paginator import Paginator


from solve.models import Algorithm, AlgorithmImage, Solution, Tag

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
        algo_detailaa = request.POST.get('contents')
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




def solutions(request):

    return render(request,"solve/solutions.html")




# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.forms.models import model_to_dict
# @csrf_exempt
# def ajaxGet(request):
#     # QuerySet [] 상태의 c 
#     c = Course.objects.all()
    
#     data = []
#     # model_to_dict - 조회된 데이터를 딕셔너리 형태로 변경
#     for i in c:
#         transformedData = model_to_dict(i)
#         data.append(transformedData)

#     return JsonResponse(data, safe=False)


# def ajaxExam(request):
    
#     return render(request, 'secondapp/ajax_exam.html')


def problem_upload_complete(request):
    
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