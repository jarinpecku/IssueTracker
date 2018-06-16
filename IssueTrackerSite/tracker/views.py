from datetime import datetime, timedelta

from django.views import generic
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from .models import Issue, Status


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'issues_list'
    title = "All reported issues"
    average_time = 0

    def get_login_url(self):
        return reverse('tracker:login')

    def get_queryset(self):
        """Return the last five published questions."""
        return Issue.objects.order_by('-created')

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context.update(compute_stats(Issue.objects))
        return context


class MyIssuesView(LoginRequiredMixin, generic.ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'issues_list'
    title = "Issues assigned to me"

    def get_login_url(self):
        return reverse('tracker:login')

    def get_queryset(self):
        return Issue.objects.filter(assigned_to=self.request.user).order_by('-created')


class NewIssuesView(LoginRequiredMixin, generic.ListView):
    template_name = 'tracker/index.html'
    context_object_name = 'issues_list'
    title = "New issues"

    def get_login_url(self):
        return reverse('tracker:login')

    def get_queryset(self):
        return Issue.objects.filter(status=1).order_by('-created')


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

    def get_success_url(self):
        return reverse('tracker:detail', args=[self.object.id])

    def get_login_url(self):
        return reverse('tracker:login')


class UpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Issue
    fields = ['title', 'assigned_to', 'description', 'status', 'category']
    template_name = 'tracker/update_form.html'
    permission_required = 'Issue.is_superuser'

    def get_success_url(self):
        return reverse('tracker:detail', args=[self.object.id])

    def get_login_url(self):
        return reverse('tracker:login')

    def form_valid(self, form):
        if form.instance.status.name == 'closed':
            form.instance.closed = datetime.now()

        return super(UpdateView, self).form_valid(form)


class DeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Issue
    template_name = 'tracker/delete.html'
    permission_required = 'Issue.is_superuser'

    def get_success_url(self):
        return reverse('tracker:index')

    def get_login_url(self):
        return reverse('tracker:login')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('tracker:index')


def datetime_division(value, denom):
    """
    Implements datetime division.

    Args:
        value (datetime): datetime value to divide
        denom (int, float): denominator

    Returns:
         datetime
    """
    total_seconds = (value.microseconds + (value.seconds + value.days * 24 * 3600) * 1e6) / 1e6
    divided_seconds = total_seconds / float(denom)
    return timedelta(seconds=divided_seconds)


def compute_stats(issues):
    """
    Compute min, max, and average issue solving times.

    Args:
        issues (Issue.objects): list of all issues from DB

    Returns:
        dict: dictionary with stats
                {'min': int, 'avg': int, 'max': int}
    """
    closed_issues = issues.filter(status=Status.get_closed_id())
    times = [issue.closed - issue.created for issue in closed_issues]

    total_time = timedelta(days=0)
    for td in times:
        total_time += td

    return {'min': min(times),
            'avg': datetime_division(total_time, len(times)),
            'max': max(times)}
