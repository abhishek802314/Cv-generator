from django.shortcuts import render, HttpResponse
from .models import Profile
import pdfkit
from django.template import loader
import io
# Create your views here.

def accept(request):
    if request.method =='POST':
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summary", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")
        
        profile = Profile(name=name, email=email, phone=phone, summary=summary,degree=degree,
                           school=school, university=university, previous_work=previous_work, skills=skills)
        profile.save()
    return render(request, 'pdfapp/accept.html')

def resume(request, pk):
    user_profile = Profile.objects.get(id=pk)
    context = {'user_profile':user_profile}
    template = loader.get_template('pdfapp/resume.html')
    html = template.render(context)
    options = {
        'page-size':'Letter',
        'encoding':'UTF-8',
    }
    config = pdfkit.configuration(wkhtmltopdf=b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(html, False, options=options, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = 'resume.pdf'
   
    return response


def list(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'pdfapp/list.html', context)