from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView
from .models import Home

# Create your views here.
class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ctx'] = Home.objects.all()
        return context
    

def home(request):
    home = Home.objects.all()
    return render(request, 'core/home.html', {'Home':home})