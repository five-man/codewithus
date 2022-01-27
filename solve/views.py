import datetime
import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from config.settings import MEDIA_ROOT, STATIC_ROOT
from member.models import Member
from django.contrib import messages

from solve.models import Algorithm, AlgorithmImage, Tag

# Create your views here.
def problem_list(request):

    return render(request,"solve/problem_list.html")

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
