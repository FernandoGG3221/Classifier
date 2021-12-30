from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import PageModel
from .forms import PageForm
from django.urls import reverse_lazy


class StaffRequiredMixin(object):
    ## Requiere que el usuario sea miembro del staff

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin,self).dispatch(request,*args,**kwargs)

# Create your views here.
##El metodo dispatch sirve para controlar la petición

@method_decorator(staff_member_required, name='dispatch')
class PageListView(ListView):
    model = PageModel
    
class PageDetailView(DetailView):
    model = PageModel

@method_decorator(staff_member_required, name='dispatch')
class PageCreateView(CreateView):
    model = PageModel
    form_class = PageForm
    success_url = reverse_lazy('pages:pages')

@method_decorator(staff_member_required, name='dispatch')
class PageUpdateView(UpdateView):
    model = PageModel
    form_class = PageForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        print('self onject id = ',self.object.id)
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'

@method_decorator(staff_member_required, name='dispatch')
class PageDeleteView(DeleteView):
    model = PageModel
    success_url = reverse_lazy('pages:pages')