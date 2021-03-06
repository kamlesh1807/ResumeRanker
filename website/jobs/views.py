from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Job , Resume

from django.shortcuts import redirect

from django.http import JsonResponse
import json, spacy, math, logging
import PyPDF2, re, docx2txt
from django.conf import settings
nlp = spacy.load("en_core_web_sm")
# Create your views here.

from .tasks import scoringResumes

@login_required
def jobs_view(request):
    
    if request.method == "GET":
        jobs = list(Job.objects.filter(user=request.user).values())
        print(jobs)
        return render(request, 'app/jobs.html',{"jobs":jobs})
    
    if request.method == "POST":
        title = request.POST.get("title")
        job_description = request.POST.get("job_description")
        skills = request.POST.get("skills")
        insertObject = Job.objects.create(user=request.user,title=title,job_description=job_description,skills=skills)
        jobs = list(Job.objects.filter(user=request.user).values())
        return render(request, 'app/jobs.html',{"jobs":jobs})

@login_required
def jobDetail(request, pk):
    if request.method == "GET":
        current_job = Job.objects.get(user=request.user,id=pk)
        job = list(Job.objects.filter(user=request.user, id=pk).values())[0]
        resumes = list(Resume.objects.filter(job=current_job).values())
        return render(request, 'app/job.html',{"job": job,"resumes":resumes})
    
    if request.method == "POST":
        current_job = Job.objects.get(user=request.user,id=pk)
        job = list(Job.objects.filter(user=request.user, id=pk).values())[0]
        for f in request.FILES.getlist('files'):
            exist , email, matchedSkills, data = fetchData(f,job['skills'], pk)
            if  exist :
                Resume.objects.create(job=current_job,email=email,skills=matchedSkills,resume_data=data)
        resumes = list(Resume.objects.filter(job=current_job).values())
        return render(request, 'app/job.html',{"job": job,"resumes":resumes})

    
@login_required
def jobDelete(request, pk):
    Job.objects.filter(id=pk).delete()
    jobs = list(Job.objects.filter(user=request.user).values())
    return redirect('/jobs')
    
    #return render(request, 'app/jobs.html',{"jobs":jobs})


def fetchData(resume, skills , pk):
    
    skills = skills.split(",")
    data = ""
    
    if resume.name[-3:].lower() == "pdf" :
        pdfReader = PyPDF2.PdfFileReader(resume.file)
        number_of_pages = pdfReader.getNumPages()
        for page in range(number_of_pages):
            page = pdfReader.getPage(page)
            data += page.extractText()
        email = re.search(r'[\w\.-]+@[\w\.-]+', data).group(0)
        matchedSkills = ",".join([skill for skill in skills if skill.lower() in data.lower()])
        if Resume.objects.filter(email=email, job=pk).exists():
            return False, email, matchedSkills, data
        else :
            return True, email, matchedSkills, data


    if resume.name[-4:].lower() == "docx":
        data = docx2txt.process(resume.file)

        email = re.search(r'[\w\.-]+@[\w\.-]+', data).group(0)
        matchedSkills = ",".join([skill for skill in skills if skill.lower() in data.lower()])
        if Resume.objects.filter(email=email, job=pk).exists():
            return False, email, matchedSkills, data
        else :
            return True, email, matchedSkills, data


@login_required
def resumeDelete(request, jid, rid):
    Resume.objects.filter(id=rid).delete()
    return redirect('/job/{}'.format(jid))




@login_required
def checkScoringStatus(request, jid):

    job = list(Job.objects.filter(user=request.user, id=jid).values())[0]

    if job['status'] == "SCORING":
        status = True
    else:
        status = False

    return JsonResponse({"status": status})


       
      

@login_required
def scoring(request, jid):
    user = request.user.get_username()
    scoringResumes.delay(user, jid)
    return redirect('/job/{}'.format(jid))

