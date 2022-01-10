from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from .models import User
# Create your views here.

def index(request):
    return render(request, "acc/index.html")

def userlogin(request):
    if request.method == "POST":
        un = request.POST.get("un")
        pw = request.POST.get("pw")
        user = authenticate(username=un, password=pw)
        if user:
            login(request,user)
            return redirect("acc:index")
        else:
            pass
    return render(request, "acc/login.html")

def userlogout(request):
    logout(request)
    return redirect("acc:index")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("un")
        pw = request.POST.get("pw")
        userpic = request.FILES.get("userpic")
        age = request.POST.get("age")
        comment = request.POST.get("comment")
        User.objects.create_user(username=un, password=pw, pic=userpic, age=age, comment=comment)   # 패스워드 암호화 된 상태에서 넘겨주기 위해 (왼쪽은 table field명)
        return redirect("acc:login")
    return render(request, "acc/signup.html")

def profile(request):        
    return render(request, "acc/profile.html")

def delete(request):
    # request.user.delete()
    pw = request.POST.get("pw")
    if check_password(pw, request.user.password):
        request.user.delete()
    else:
        pass
    # print(check_password(pw, request.user.password))
    return redirect("acc:index")

def update(request):
    if request.method == "POST":
        u = request.user
        pw = request.POST.get("pw")
        if pw:
            u.set_password(pw)
        comment = request.POST.get("comment")
        u.comment = comment
        pic = request.FILES.get("userpic")
        if pic:
            u.pic.delete()      # 사진을 추가하면 기존 사진 삭제되는 기능
            u.pic = pic
        u.save()
        login(request,u)
        return redirect("acc:profile")
    return render(request, "acc/update.html")
