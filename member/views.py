from django.shortcuts import render

# Create your views here.
def main(request):

    return render(request,"member/main.html")

def login(request):

    return render(request,"member/login.html")

def signup(request):

    return render(request,"member/signup.html")