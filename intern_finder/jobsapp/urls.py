from django.urls import path, include

from .views import *

from . import views

app_name = "jobs"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='searh'),
    path('employer/dashboard', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('all-applicants', ApplicantsListView.as_view(), name='employer-all-applicants'),
        path('applicants/<int:job_id>', ApplicantPerJobView.as_view(), name='employer-dashboard-applicants'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
    ])),
    path('apply-job/<int:job_id>', ApplyJobView.as_view(), name='apply-job'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('jobs/<int:id>/', JobDetailsView.as_view(), name='jobs-detail'),
    path('employer/jobs/create', JobCreateView.as_view(), name='employer-jobs-create'),
    path('about-us/', views.about_us, name='about_us'),  # Include app namespace
    path('contact-us/', views.contact_us, name='contact_us'),  # Include app namespac
     path('delete/<int:job_id>/', views.delete_job, name='delete-job'),
     path('edit/<int:job_id>/', edit_job, name='edit-job'),
     
     path('employer/dashboard/', DashboardView.as_view(), name='employer-dashboard'),
     path('employer/home/', employer_home_view, name='employer_home'),
    path('jobs/<int:job_id>/', JobDetailsView.as_view(), name='jobs-detail'),
    
]
