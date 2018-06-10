from django.contrib import admin
from django import forms

from .models import Issue, Status, Category


#class IssueModelForm(forms.ModelForm):
#    description = forms.CharField(widget=forms.Textarea)
#
#    class Meta:
#        model = Issue


#class IssueAdmin(admin.ModelAdmin):
#    form = IssueModelForm


#admin.site.register(Issue, IssueAdmin)
admin.site.register(Issue)
admin.site.register(Status)
admin.site.register(Category)
