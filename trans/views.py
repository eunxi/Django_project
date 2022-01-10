from django.shortcuts import render
from googletrans import Translator
# Create your views here.

def index(request):
    context = {}
    if request.method == "POST":
        bef = request.POST.get("before")
        f = request.POST.get("from")
        t = request.POST.get("to")
        
        translator = Translator()
        trans1 = translator.translate(bef, src=f, dest=t)
        context.update({
            "aft" : trans1.text,        # trans1 의 text 를 가져온다는 의미!?
            "bef" : bef,
            "f" : f,
            "t" : t
        })

    return render(request, "trans/index.html", context)