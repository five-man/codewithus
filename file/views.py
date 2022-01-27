from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import File
from django.utils import timezone
from member.models import Member
from django.core.paginator import Paginator

# Create your views here.

def file(request):
    return render(request, 'file/file_list.html')

def uploadFile(request):
    if request.method == "POST":
        uploadedFile = request.FILES.get("file")
        must = Member.objects.get(member_no=1)
        name = uploadedFile.name
        
        file = File(
            file_name = name, 
            file_date = timezone.now(),
            file_volume = 0,
            member_no = must
        )
        file.save()

        with open(name, 'wb') as file: # 파일 저장
            for chunk in uploadedFile.chunks():
                file.write(chunk)

    documents = File.objects.all()

    now_page = request.GET.get('page', 1)
    now_page = int(now_page)

    p = Paginator(documents, 5)
    page_obj = p.get_page(now_page)

    start_page = (now_page-1) // 10 * 10 + 1
    end_page = start_page + 9
    if end_page > p.num_pages:
        end_page = p.num_pages

    context = {"files": page_obj,
                'page_range' : range(start_page, end_page+1)}

    return render(request, "file/file_list.html", context)
