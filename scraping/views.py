from django.views.generic import ListView

from .models import People


class LinkedInFindView(ListView):
    template_name = 'employees_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return People.objects.all()
