from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import File
from django.utils import timezone
from member.models import Member

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
    return render(request, "file/file_list.html", {"files": documents})
