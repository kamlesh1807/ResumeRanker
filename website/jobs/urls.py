from django.urls import path, re_path

from .views import jobs_view, jobDetail, jobDelete , resumeDelete, scoring,checkScoringStatus

app_name = 'jobs'

urlpatterns = [
	path('jobs/', jobs_view, name='jobs'),
	path('job/<int:pk>', jobDetail, name='jobDetail'),
	path('job/delete/<int:pk>', jobDelete, name='jobDelete'),
	path('job/<int:jid>/resume/delete/<int:rid>', resumeDelete, name='resumeDelete'),
	path('job/scoring/<int:jid>', scoring, name='scoring'),
    path('job/scoring/<int:jid>/status', checkScoringStatus, name='checkScoringStatus')
]

