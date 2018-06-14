from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from .models import Issue


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'issues_list'
    login_url = 'login/'

    def get_queryset(self):
        """Return the last five published questions."""
        return Issue.objects.order_by('-created')


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Issue
    template_name = 'tracker/detail.html'

    def get_login_url(self):
        return reverse('tracker:login')


class CreateView(PermissionRequiredMixin, generic.CreateView):
    model = Issue
    fields = ['title', 'assigned_to', 'description', 'category']
    template_name = 'tracker/create.html'
    permission_required = 'Issue.is_superuser'
    login_url = '../../login/'

    def get_success_url(self):
        return reverse('tracker:detail', args=[self.object.id])

    def get_login_url(self):
        return reverse('tracker:login')


class UpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Issue
    fields = ['title', 'assigned_to', 'description', 'status', 'category']
    template_name = 'tracker/update_form.html'
    permission_required = 'Issue.is_superuser'
    login_url = '../../login/'

    def get_success_url(self):
        return reverse('tracker:detail', args=[self.object.id])

    def get_login_url(self):
        return reverse('tracker:login')


class DeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Issue
    template_name = 'tracker/delete.html'
    permission_required = 'Issue.is_superuser'
    login_url = '../../login/'

    def get_success_url(self):
        return reverse('tracker:index')

    def get_login_url(self):
        return reverse('tracker:login')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = '../'
    template_name = 'registration/signup.html'
