from distutils import filelist
from importlib.resources import path
from django.forms import FilePathField
from django.shortcuts import render
from django.http import HttpResponse, response
from django.core.files.storage import FileSystemStorage
from sqlalchemy import null
from .models import File, FileList
from django.utils import timezone
from member.models import Member
import os
from config import settings
from config.settings import MEDIA_ROOT
from django.contrib import messages

# Create your views here.

# def file(request):
#     return render(request, 'file/file_list.html')

def uploadFile(request):
    if request.method == "POST":
        uploadedFile = request.FILES.get("file")
        fileTitle = request.POST["fileTitle"]
        now_member = request.session['member_no']
        must = Member.objects.get(member_no = now_member)
        name = uploadedFile.name
        file_root = os.path.join(MEDIA_ROOT)
        
        try:
            new_name = FileList.objects.get(file_name = name)
            new_name = str("new") + str(new_name.file_name)
        except FileList.DoesNotExist:
            new_name = name

        file = File(
            file_name = fileTitle,
            file_date = timezone.now(),
            file_volume = uploadedFile.size,
            file_root = file_root,
            member_no = must
        )
        file.save()

        fileno = File.objects.latest('file_no')
        fileroot = File.objects.latest('file_root')
        filelist = FileList(
            file_name = new_name,
            file_no = fileno,
            file_root = fileroot.file_root
        )

        try:
            with open(file_root+"wer/"+name, 'wb') as piz: # 파일 저장
                for chunk in uploadedFile.chunks():
                    piz.write(chunk)
        except FileNotFoundError:
            file.delete()
            messages.info(request, '정보를 나타냅니다.')

        filelist.save()
    filelist = FileList.objects.all()
    return render(request, "file/file_list.html", {"filelist": filelist})


def download(request):
    if request.method == 'POST':
        fn = request.POST["filename"]
        filename = FileList.objects.get(file_name = fn)
        filepath = str(settings.BASE_DIR) + ('\\media\\%s' % filename.file_name)
        with open(filepath, 'rb') as f:
            response = HttpResponse(f, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=%s' % fn
    return response