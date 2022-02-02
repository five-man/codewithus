import datetime
from distutils import filelist
from email import message
from importlib.resources import path
from django.forms import FilePathField
from django.shortcuts import redirect, render
from django.http import HttpResponse, response
from django.core.files.storage import FileSystemStorage
from sqlalchemy import null
from .models import File, FileList
from django.utils import timezone
from member.models import Member
import os, urllib
from config import settings
from config.settings import MEDIA_ROOT
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

# def file(request):
#     return render(request, 'file/file_list.html')

def uploadFile(request):
    if request.method == "POST":
        uploadedFile = request.FILES.get("file")
        title = request.POST["title"]
        now_member = request.session['member_no']
        must = Member.objects.get(member_no = now_member)
        filename = uploadedFile.name
        file_root = os.path.join(MEDIA_ROOT)
        
        try:
            FileList.objects.get(file_name = filename)
        except FileList.DoesNotExist:
            new_name = filename

            file = File(
                file_name = title,
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
                with open(file_root+"/"+filename, 'wb') as piz: # 파일 저장
                    for chunk in uploadedFile.chunks():
                        piz.write(chunk)
            except FileNotFoundError:
                file.delete()
                # messages.info(request, '정보를 나타냅니다.')
            filelist.save()
            messages.success(request, 'upload-success')
            return redirect('file:file_upload')
        messages.warning(request, 'upload-fail')
        return redirect('file:file_upload')
    filelist = FileList.objects.all()
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
                'page_range' : range(start_page, end_page+1), "filelist": filelist}

    return render(request, "file/file_list.html", {"filelist": filelist})

def download(request):
    if request.method == 'POST':
        fn = request.POST["filename"]
        filename = FileList.objects.get(file_name = fn)
        filepath = str(settings.BASE_DIR) + ('/media/%s' % filename.file_name)
        fn = urllib.parse.quote(fn.encode('utf-8'))
        with open(filepath, 'rb') as f:
            response = HttpResponse(f, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % fn
    return response

def delete(request):
    if request.method == 'POST':
        filename = request.POST["filename"]
        listrow = FileList.objects.get(file_name = filename)
        filerow = File.objects.get(file_no = listrow.file_no.file_no)
        now_member = Member.objects.get(member_no = request.session['member_no'])
        if (now_member.admin_flag == 1) or (filerow.member_no.member_no == now_member.member_no):
                filepath = str(settings.BASE_DIR) + ('/media/%s' % filename)
                # DB삭제
                listrow.delete()
                filerow.delete()
                # 파일 삭제
                os.remove(filepath)
                return redirect('file:file_upload')
        else:
            messages.warning(request, 'member-fail')
            return redirect('file:file_upload')