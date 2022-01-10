from django.shortcuts import render
import pdfplumber
# Create your views here.

def index(request):
    context = {}    # context 딕셔너리 생성
    if request.method == "POST":
        p = request.FILES.get("pdf")
        pdf = pdfplumber.open(p)
        text = ""
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text += page.extract_text()
            text += "="*30 + f"{i+1} Page Text" + "="*30 +"\n"
        pdf.close()
        context["t"] = text # 하나만 추가 및 넘겨줄 것이므로 이렇게 넘겨주고, 여러개 추가 및 넘겨줄 때는 context.update[{}]
    return render(request,"pdfread/index.html", context)