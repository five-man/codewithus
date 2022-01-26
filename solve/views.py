import datetime
import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from config.settings import MEDIA_ROOT
from member.models import Member

from solve.models import Algorithm, AlgorithmImage, Tag

# Create your views here.
def problem_list(request):

    return render(request,"solve/problem_list.html")

def problem_upload(request):
    #print(request.session['member_no'])
    #
    #   오늘의 문제가 있다면 업로드 못하게 막는 로직
    #
    
    if request.method == 'POST':
        algo_title = request.POST.get('subject')
        algo_detail = request.POST.get('contents')
        tag = request.POST.get('algorithm_tag')
        member_no = request.session.get('member_no')
        uploadedFile= request.FILES.getlist("image")
        
        #
      
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        
        # a = Algorithm(
        #     algo_title=algo_title, 
        #     algo_detail=algo_detail, 
        #     member_no=Member.objects.get(member_email=member_email,member_name=member_name),
        #     tag_id = Tag.objects.filter(name__contains=tag)
        # )
        
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
                image_root= "/media/",
                algo_no=Algorithm.objects.get(algo_no=8))
            i.save()
            save_path = os.path.join(MEDIA_ROOT,i.image_name)
            with open(save_path, 'wb') as file:
                for chunk in uploadFile.chunks():
                    file.write(chunk)
            
        # 글이 써지면 오늘의 문제로 
        return redirect('/solve/today_exam/')
    else:
        # 
        return render(request, 'solve/problem_upload.html')

    # return render(request,"solve/problem_upload.html")

def today_exam(request):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    
    today_algo = Algorithm.objects.get(algo_update = '2021-12-07')
    algo_image_object = AlgorithmImage.objects.filter(algo_no= today_algo)
    # algo_image_object.
    # print(today_algo)
    
    return render(request, 'solve/today_exam.html', {'image':algo_image_object})

    
    
    
    
    
    return render(request,"solve/today_exam.html")

# if __name__ =="__main__":
#     problem_upload(request)