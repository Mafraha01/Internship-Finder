from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView

from jobsapp.forms import ApplyJobForm
from jobsapp.models import Job, Applicant

from django.shortcuts import render

from django.shortcuts import get_object_or_404


from jobsapp.models import Applicant, Job
from jobsapp.forms import ApplyJobForm

from django.urls import reverse_lazy

class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.all()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
        return context


class SearchView(ListView):
    model = Job
    template_name = 'jobs/search.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.filter(location__contains=self.request.GET['location'],
                                         title__contains=self.request.GET['position'])


class JobListView(ListView):
    model = Job
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 5


class JobDetailsView(DetailView):
    model = Job
    template_name = 'jobs/details.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from jobsapp.models import Applicant, Job
from jobsapp.forms import ApplyJobForm


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    template_name = 'jobs/details.html'  # Update with your template name

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Redirect to the job details page after successful application
        return reverse('jobs:jobs-detail', kwargs={'job_id': self.kwargs['job_id']})

    def form_valid(self, form):
        # Ensure that the user has not already applied for this job
        job_id = self.kwargs['job_id']
        if Applicant.objects.filter(user=self.request.user, job_id=job_id).exists():
            messages.info(self.request, 'You have already applied for this job.')
            return HttpResponseRedirect(self.get_success_url())
        
        # Save the applicant with the current user and job
        form.instance.user = self.request.user
        form.instance.job_id = job_id
        form.save()

        messages.success(self.request, 'Successfully applied for the job!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the job object to the template for rendering
        job_id = self.kwargs['job_id']
        job = get_object_or_404(Job, pk=job_id)
        context['job'] = job
        return context

    
def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    return render(request, 'contact_us.html')


from django.shortcuts import redirect, get_object_or_404
from jobsapp.models import Job

def delete_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('jobs:employer-dashboard')  # Redirect to the homepage or any other suitable page
    else:
        return redirect('jobs:home')

from django.shortcuts import render, redirect
from jobsapp.models import Job
from jobsapp.forms import JobForm

def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('jobs:employer-dashboard')  # Redirect to the dashboard or wherever you want
    else:
        form = JobForm(instance=job)  # Pass instance to prefill the form fields
    return render(request, 'edit_job.html', {'form': form})


from django import forms
from jobsapp.models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'filled', 'last_date']  # Update with your desired fields

from django.shortcuts import render
from jobsapp.forms import ApplyJobForm  # Import your ApplicantForm if you have one

def apply_job(request, job_id):
    # Your view logic here
    if request.method == 'POST':
        # Process form submission
        form = ApplyJobForm(request.POST)
        if form.is_valid():
            # Save the form data
            form.save()
            # Redirect to a success page or any other appropriate action
            return HttpResponseRedirect('/success/')
    else:
        # Render the form for GET request
        form = ApplyJobForm()
    
    return render(request, 'jobsapp/applicant.html', {'form': form})

from django.shortcuts import render

def dashboard_view(request):
    # Your view logic here, if needed
    return render(request, 'jobsapp/dashboard.html')

def employer_home_view(request):
    return render(request, 'jobsapp/home_employer.html')