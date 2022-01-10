from django.shortcuts import redirect, render
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def index(request):
    pg = request.GET.get("page",1)
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw","")
    if cate == "sub":
       b = Board.objects.filter(subject__startswith=kw)
    # elif cate == "wri":
    #     b = Board.objects.filter(writer=kw)   # kw 랑 writer 비교는 객체(acc/models.py 전체)와 문자열을 비교하는 것과 같다.
    elif cate == "con":
        b = Board.objects.filter(content__contains=kw)
    else: 
        b = Board.objects.all()
    b = b.order_by('-pubdate')  # 레코드들에다 .order_by() : 어떤 항목에 대해서 정렬할 것인지 설정 -> 'field' '-field'(새로운 글이 먼저 나타나도록)
    pag = Paginator(b, 10)
    obj = pag.get_page(pg)
    context = {
        "blist" : obj,
        "cate" : cate,
        "kw" : kw
    }
    return render(request,"board/index.html",context)

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "bo" : b,
        "rlist" : r
    }
    return render(request, "board/detail.html", context)

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
    else:   # 메세지 시간에 넣어주기 (경고창)
        messages.warning(request,"No Hack")
    return redirect("board:index")

def create(request):
    if request.method == "POST":
        sub = request.POST.get("sub")
        con = request.POST.get("con")
        if sub:
            Board(subject=sub, writer=request.user, content=con, pubdate=timezone.now()).save() # request.user : 지금 사용중인 유저 넣어주는 것 (변경 절대 불가)
        else:
            messages.info(request,"No Subjects can't make board")
        return redirect("board:index")
    # print(request.POST)
    return render(request, "board/create.html")

def update(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer != request.user:
        messages.warning(request, "No Hack")
        return redirect("board:index")
        
    if request.method == "POST":
        b.subject = request.POST.get("sub")
        b.content = request.POST.get("con")
        b.save()
        return redirect("board:detail",bpk=bpk)
    context = {
        "bo" : b
    }
    return render(request, "board/update.html",context)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    com = request.POST.get("com")
    Reply(b=b, replyer=request.user, comment=com, pubdate=timezone.now()).save()  # request.user : 지금 작성 중인 사람

    return redirect("board:detail", bpk=bpk) # board 는 bpk 를 가지고 있기 때문에, bpk=bpk 작성

def dreply(request, bpk, rpk):  # bpk = b.writer // rpk = r.replyer
    r = Reply.objects.get(id=rpk)
    if request.user == r.replyer:
        r.delete()
    else:
        messages.warning(request,"No Hack")
    return redirect("board:detail", bpk=bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user) # 지금 유저가 좋아요 눌렀을 때 실행되도록 코드 작성
    return redirect("board:detail", bpk=bpk)

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user) # 지금 유저가 좋아요 취소 눌렀을 때 실행
    return redirect("board:detail", bpk=bpk)