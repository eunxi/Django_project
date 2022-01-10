from django.shortcuts import redirect, render
from .models import Topic, Choice
from django.utils import timezone
# Create your views here.

def cancel(request, tpk):
    t = Topic.objects.get(id=tpk)
    u = request.user
    if u in t.voter.all():  # 투표했을 경우, 유저를 투표자에서 제거해주기
        t.voter.remove(u)
        u.choice_set.get(subject=t).choicer.remove(u)   # user 입장에서 내가 고른 choice 다 나와 -> 근데 choice 중에 subject 가 t 인 애 가져와 -> 레코드 한줄 다 가져와진다.(Class Choice) -> .choicer 해주면 choicer 만 가져오는 것이고, 이 중에서 remove(u) 해줬으니 u(user = 나)를 제거해주세요~
        # _set: choice 는 가만히 있는데 user 때문에 나오라고 당할 때 사용하는 코드로, _set 사용 안하려면 (models.py에서) related_name 줘야한다.
    return redirect("vote:detail", tpk=tpk)

def create(request):
    if request.method == "POST":
        sub = request.POST.get("sub")
        con = request.POST.get("con")
        t = Topic(subject=sub, writer=request.user, pubdate=timezone.now(), content=con)
        names = request.POST.getlist("cho_name")    # getlist 를 해줘야 여러 개의 name 가져오기 가능
        coms = request.POST.getlist("cho_com")
        pics = request.FILES.getlist("cho_pic")
        t.save()
        for name, com, pic in zip(names, coms, pics):   # 1회 반복 때는 1번째의 name, com, pic 들어간다...(반복)
            Choice(subject=t, name=name, pic=pic, comment=com).save()   # Choice 의 subject 는 Topic 이 필요하기 때문에, subject=t 라고 해줌. t는 위에서 Topic 을 받는다.
        return redirect("vote:index")
    return render(request, "vote/create.html")

def vote(request, tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():   # 투표자에 유저가 없다면 투표하게 만들어주기
        t.voter.add(request.user)           # 투표자에 추가
        cho = request.POST.get("cho")
        c = Choice.objects.get(id=cho)
        c.choicer.add(request.user) # 선택자에 추가 -> 취소를 위해서 객체 생성해준 것!
    return redirect("vote:detail", tpk=tpk)

def detail(request,tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()      # 참조해줄 때 사용
    context = {
        "to" : t,
        "clist" : c
    }
    return render(request, "vote/detail.html", context)

def index(request):
    t = Topic.objects.all()
    context = {
        "tlist" : t
    }
    return render(request, "vote/index.html", context)