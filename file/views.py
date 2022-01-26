from distutils import filelist
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import File, FileList
from django.utils import timezone
from member.models import Member

# Create your views here.

# def file(request):
#     return render(request, 'file/file_list.html')

def uploadFile(request):
    if request.method == "POST":
        uploadedFile = request.FILES.get("file")
        must = Member.objects.get(member_no=1)
        name = uploadedFile.name
        file = File(
            file_name = uploadedFile.name,
            file_date = timezone.now(),
            file_volume = uploadedFile.size,
            member_no = must
        )
        file.save()

        with open(name, 'wb') as file: # 파일 저장
            for chunk in uploadedFile.chunks():
                file.write(chunk)
    must = Member.objects.get(member_no=1)
    filelist = FileList.objects.all()
    return render(request, "file/file_list.html", {"filelist": filelist})
