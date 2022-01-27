import datetime, json, os
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from numpy import save
from config.settings import BASE_DIR, MEDIA_ROOT
from solve.models import Algorithm, AlgorithmImage, Comment, Solution
from member.models import Member
from django.db.models import Count
from django.core import serializers

# Create your views here.


def problem_list(request):

    return render(request, "solve/problem_list.html")


def problem_upload(request):

    #
    #   오늘의 문제가 있다면 업로드 못하게 막는 로직
    #

    if request.method == 'POST':
        algo_title = request.POST.get('subject')
        algo_detail = request.POST.get('contents')
        member_no = request.session.get('member_no')
        uploadedFile = request.FILES.getlist("image")

        a = Algorithm(
            algo_title=algo_title,
            algo_detail=algo_detail,
            member_no=Member.objects.get(member_no=member_no),
            tag_id=3,
            algo_update=timezone.now())
        a.save()

        for uploadFile in uploadedFile:
            # image_name =
            i = AlgorithmImage(
                image_name=uploadFile.name,
                image_root="/media/",
                algo_no=Algorithm.objects.get(algo_no=87))
            i.save()
            save_path = os.path.join(MEDIA_ROOT, i.image_name)
            with open(save_path, 'wb') as file:
                for chunk in uploadFile.chunks():
                    file.write(chunk)

        # 글이 써지면 오늘의 문제로
        return redirect('/today_exam/')
    else:
        #
        return render(request, 'solve/problem_upload.html')

    # return render(request,"solve/problem_upload.html")


def today_exam(request):

    # now = datetime.datetime.now()
    # nowDate = now.strftime('%Y-%m-%d')

    # today_algo = Algorithm.objects.get(algo_no = 87)
    # algo_image_object = AlgorithmImage.objects.filter(algo_no=today_algo)

    # return render(request, 'solve/today_exam.html', {'image':algo_image_object.image_name})

    return render(request, "solve/today_exam.html")


def solutions(request, algo_no=50):
    solution = Solution.objects.filter(algo_no = algo_no)

    reply = Comment.objects.filter(sol_no__in = solution)

    try:
        session = request.session.get('member_no')
        context = {
            'solutions': solution,
            'reply': reply,
            'session': session,
        }
        return render(request, 'solve/solutions.html', context)
    except KeyError:
        return redirect('member/main')

def reply(request):
    member_no = request.session.get('member_no')
    jsonObject = json.loads(request.body)
    solno = jsonObject.get('sol_no')
    reply = Comment.objects.create(
        sol_no=Solution.objects.get(sol_no=solno),
        # algo_no=Solution.objects.get(algo_no=50),
        algo_no=Solution.objects.get(sol_no=solno),
        member_no=Member.objects.get(member_no=member_no),
        comment_detail=jsonObject.get('comment_detail'),
    )
    reply.save()
    membername = Member.objects.get(member_no = member_no)
    context = {
        # 'name': serializers.serialize("json", reply.member_no),
        #'content': reply.comment_detail,
        'pp': membername.member_name    
    }

    return JsonResponse(context)
