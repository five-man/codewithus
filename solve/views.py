from django.shortcuts import render

# Create your views here.
def problem_list(request):

    return render(request,"solve/problem_list.html")

def problem_upload(request):

    return render(request,"solve/problem_upload.html")

def today_exam(request):

    return render(request,"solve/today_exam.html")