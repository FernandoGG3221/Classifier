from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import RedirectView
from .models import *
from .forms import ProjectForm, BancoImageForm, ImageForm
from django.urls import reverse, reverse_lazy
import os, sys
import subprocess
from django.http import HttpResponseRedirect

# Create your views here.
class ProjetcsListView(ListView):
    model = Proyecto
    
    def get_queryset(self):
        autor = self.request.user
        print('Autor: ',autor)
        return Proyecto.objects.filter(FK_autor = self.request.user)

class ProjectDetailView(DetailView):
    model = Proyecto

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        print('Contexto: ', context)
        titulo = context.get('proyecto')
        #print('Titulo del proyecto: ',titulo)        
        context['img'] = Imagen.objects.filter(FK_proyecto = titulo)
        #print('Contexto: ', context)
        return context

class ProjectCreateView(CreateView):
    model = Proyecto
    form_class = ProjectForm
    success_url = reverse_lazy('projects:projects')

    def post(self,request):
        form_class = ProjectForm
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            if form.is_valid():
                form.instance.FK_autor = request.user
                try:
                    # --- Etiqueta uno ---
                    #t1 = Etiqueta_uno(tag = form.cleaned_data['tag_uno'])
                    #t1.save()

                    #form.instance.FK_tag_uno = t1

                    # -- Etiqueta dos ---
                    #t2 = Etiqueta_dos(tag = form.cleaned_data['tag_dos'])
                    #t2.save()

                    #form.instance.FK_tag_dos = t2

                    # --- Etiqueta tres ---
                    #t3 = Etiqueta_tres(tag = form.cleaned_data['tag_tres'])
                    #t3.save()

                   # form.instance.FK_tag_tres = t3
                    print('entrando al Try')
                    proyecto = form.save()
                    print('proyecto: ', proyecto)
                    #t1 = Etiqueta(tag = form.cleaned_data['tag_uno'], FK_proyecto = )
                    Etiqueta.objects.bulk_create([
                        Etiqueta(tag = form.cleaned_data['tag_uno'],FK_proyecto = proyecto),
                        Etiqueta(tag = form.cleaned_data['tag_dos'],FK_proyecto = proyecto),
                        Etiqueta(tag = form.cleaned_data['tag_tres'],FK_proyecto = proyecto),
                    ])
                    # --- Guardamos el objeto ---
                    form.save() 
                    print('Form: ', form)
                    
                except:
                    print('error')
                
            return self.form_valid(form)
        return self.form_invalid(form)

class ProjectDeleteView(DeleteView):
    model = Proyecto
    success_url = reverse_lazy('projects:projects') 

    #Clases de almacenamiento de imágenes.


class BancoImagesView(UpdateView):
    model = Proyecto
    form_class = BancoImageForm
    template_name = 'projects/repositorio_form.html'

    def get_object(self):
        #Recuperar el objeto que se va a editar
        a = Proyecto.objects.get(id = self.kwargs['pk'])
        return a

    def get_context_data(self, **kwargs):
        context = super(BancoImagesView, self).get_context_data(**kwargs)
        print('Contexto: ',context,'\n')
        
        titulo = context.get('proyecto')
        context['tag'] = Etiqueta.objects.filter(FK_proyecto = titulo)
        print('Contexto: ',context,'\n')
        print('KWargs: ',kwargs, '\n')
        return context

    def get_success_url(self, *args, **kwargs):          #corregir
        #Return the URL to redirect to after processing a valid form.
        a = Proyecto.objects.get(id = self.kwargs['pk'])
        queryset = None
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        print('Get pk: ',pk)
        slug = self.kwargs.get(self.slug_url_kwarg)
        print('self.object ', slug)
        return reverse('projects:project', kwargs={'pk':pk, 'slug': slug} ) + '?ok'

    #def get_success_url(self, args, kwargs):
        #print('Kwargs url: ',kwargs)
        #return reverse_lazy('projects:project', args=[self.object.pk]) + '?ok'

    def post(self,request, pk, slug, **kwargs ):
        form_class = BancoImageForm
        if request.method == 'POST':
            form = BancoImageForm(request.POST, request.FILES)

            #obtener la lista de archivos que se almacenan en el banco de imágenes
            files = request.FILES.getlist('repositorio')
            print('Archivos: ',files)

            #obtener el objeto
            self.object = self.get_object()

            #filtrar las etiquetas por proyecto
            tag = Etiqueta.objects.filter(FK_proyecto = self.object)

            #Validacion del formulario
            if form.is_valid():

                #vincula el nombre del proyecto con la llave foranea
                form.instance.FK_proyecto = self.object
                #<<<<<<<<<<<<Quitar Este>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><
                #a = form.instance.FK_proyecto

                #Obtiene la etiqueta seleccionada
                tag = form.cleaned_data['Etiqueta']
                print('Etiqueta: ', tag)

                #almacena cada uno de los archivos seleccionados
                for f in files:
                    gallery = Repositorio(FK_proyecto = self.object, Etiqueta = tag, repositorio=f)
                    print('galeria: ',gallery)
                    gallery.save()
                    print('almacenado')

                #Agregar el directorio de models
                dir_Models = os.path.abspath(r'media/banco/'+str(self.object)+'/models')
                dir_Media = os.path.abspath(r'media/banco/'+str(self.object))
                print(dir_Models)
                if os.path.exists(dir_Models):
                    print('El direcorio models ya existe!')
                else: 
                    os.mkdir(dir_Models)
                    print('Directorio models: ',dir_Models)
                return self.form_valid(form)

            else:
                return self.form_invalid(form)
                #return render(request, 'projects/repositorio_form.html', context_instance=RequestContext(request))


class ImagesView(UpdateView):
    model = Imagen
    form_class = ImageForm
    template_name = 'projects/image_form.html'

    def get_object(self, *args, **kwargs) :
        #Recuperar el objeto que se va a editar
        a = Proyecto.objects.get(id = self.kwargs['pk'])
        print('Proyecto: ',a)
        print('Kwargs get object ', kwargs)
        print('args get object ', args)
        return a
        

    def get_context_data(self, **kwargs):
        context = super(ImagesView, self).get_context_data(**kwargs)
        print('Contexto: ',context,'\n')
        
        titulo = context.get('proyecto')
        #context['img'] = Imagen.objects.filter(FK_proyecto = titulo)
        #print('Contexto: ',context,'\n')
        print('KWargs: ',kwargs, '\n')
        return context

    def get_success_url(self, *args, **kwargs):          #corregir
        #Return the URL to redirect to after processing a valid form.
        a = Proyecto.objects.get(id = self.kwargs['pk'])
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        queryset = None
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        print('pk ', pk)
        slug = self.kwargs.get(self.slug_url_kwarg)
        print('slug ', slug)
        return reverse('projects:project', kwargs={'pk':pk, 'slug': slug} )

    def post(self,request, pk, slug, **kwargs ):
        form_class = ImageForm
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)

            #obtener la lista de archivos que se almacenan en el banco de imágenes
            files = request.FILES.getlist('imagen')
            print('Archivos: ',files)

            #obtener el objeto
            self.object = self.get_object()

            #Validacion del formulario
            if form.is_valid():

                #vincula el nombre del proyecto con la llave foranea
                
                form.instance.FK_proyecto = self.object
                form.save(commit=False)

                #almacena cada uno de los archivos seleccionados
                for f in files:
                    form.save(commit = False)
                    form = Imagen(FK_proyecto = self.object,  imagen=f)
                    print('galeria: ',form)
                    form.save()
                    print('almacenado')
                return self.form_valid(form)

            else:
                return self.form_invalid(form)

class Extract_features_View(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'projects:project'

    def get_redirect_url(self, *args, **kwargs):
        #Recuperar el objeto que se va a editar
        a = Proyecto.objects.get(id = self.kwargs['pk'])
        print('Proyecto: ',a)
        
        #########   Ejecucion del script ########
        p = 'python'
        sps = '--samples'
        codebook_file = '--codebook-file'
        feature = '--feature-map-file'

        codebook_pkl = 'codebook.pkl'
        feature_PKL = 'feature_map.pkl'
        

        dir_Script = os.path.abspath('projects/custom_vision/projects')
        #print('URL directorio CV: ',dir_Script)

        dir_Media = os.path.abspath(r'media/banco/'+str(a)+'/media')
        #print('URL directorio Media: ',dir_Media)

        script_url = r''+dir_Script+'\\'+'create_features.py'
        script_url = script_url.replace('\\','/')
        print('URL script CF: ', script_url)

        tag = Etiqueta.objects.filter(FK_proyecto = a)

        tag_uno = r''+dir_Media+'\\'+str(tag[0])
        tag_uno = tag_uno.replace('\\','/')
        print('Etiqueta uno: ', tag_uno)

        tag_dos = r''+dir_Media+'\\'+str(tag[1])
        tag_dos = tag_dos.replace('\\','/')
        print('Etiqueta dos: ', tag_dos)

        tag_tres = r''+dir_Media+'\\'+str(tag[2])
        tag_tres = tag_tres.replace('\\','/')
        print('Etiqueta tres: ', tag_tres)

        dir_feature = os.path.abspath(r'media/banco/'+str(a)+'/models/'+str(feature_PKL))
        dir_feature = dir_feature.replace('\\','/')
        print('URL feature_map.pkl: ', dir_feature)

        dir_codebook = os.path.abspath(r'media/banco/'+str(a)+'/models/'+str(r''+codebook_pkl))
        dir_codebook = dir_codebook.replace('\\','/')
        print('URL Codebook.pkl: ', dir_codebook)

        try:
            print('*****Inicio de extración de catacteristicas******')
            run_script = subprocess.run([
                'python', script_url,
                sps, str(tag[0]), str(tag_uno),
                sps, str(tag[1]), str(tag_dos),
                sps, str(tag[2]), str(tag_tres),
                codebook_file, dir_codebook,
                feature, str(dir_feature)
            ])
            print('ejecucion del codigo')
            print(run_script.returncode)
            print(run_script.stdout)
            print(run_script.stderr)
            print('******************Extracción lista******************')
        except subprocess.CalledProcessError as identifier:
            print('error', identifier)

        return super().get_redirect_url(*args, **kwargs)


class Training_View(RedirectView):
    
    permanent = False
    query_string = True
    pattern_name = 'projects:project'

    def get_redirect_url(self, *args, **kwargs):
        #Recuperar el objeto que se va a editar
        a = Proyecto.objects.get(id = self.kwargs['pk'])
        print('Proyecto: ',a)
        
        #########   Ejecucion del script ########
        feature = '--feature-map-file'
        feature_PKL = 'feature_map.pkl'
        svm = '--svm-file'
        svm_PKL = 'svm.pkl'
        
        dir_Script = os.path.abspath('projects/custom_vision/projects')
        dir_Media = os.path.abspath(r'media/banco/'+str(a)+'/media')

        script_url = r''+dir_Script+'\\'+'training.py'
        script_url = script_url.replace('\\','/')

        dir_feature = os.path.abspath(r'media/banco/'+str(a)+'/models/'+str(feature_PKL))
        dir_feature = dir_feature.replace('\\','/')
        print('URL feature_map.pkl: ', dir_feature)

        dir_SVM = os.path.abspath(r'media/banco/'+str(a)+'/models/'+str(svm_PKL))
        dir_SVM = dir_SVM.replace('\\','/')
        print('URL svm.pkl: ', dir_SVM)

        try:
            print('******************Inicio de Entrenamiento de la red neuronal******************')
            run_script = subprocess.run([
                'python', script_url,
                feature, str(dir_feature),
                svm, str(dir_SVM)
            ])
            print('ejecucion del codigo')
            print(run_script.returncode)
            print(run_script.stdout)
            print(run_script.stderr)
            print('******************Entrenamiento listo******************')
        except subprocess.CalledProcessError as identifier:
            print('error', identifier)

        return super().get_redirect_url(*args, **kwargs)

class clasification_View(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'projects:project'

    def get_redirect_url(self, *args, **kwargs):
        #Recuperar el objeto que se va a editar
        a = Proyecto.objects.get(id = self.kwargs['pk'])
        print('Proyecto: ',a)
        
        #########   Ejecucion del script ########
        feature = '--feature-map-file'
        feature_PKL = 'feature_map.pkl'
        svm = '--svm-file'
        svm_PKL = 'svm.pkl'
        codebook_file = '--codebook-file'
        codebook_pkl = 'codebook.pkl'
        input = '--input-image'
        
        dir_Script = os.path.abspath('projects/custom_vision/projects')
        dir_Media = os.path.abspath(r'media/banco/'+str(a)+'/media')

        script_url = r''+dir_Script+'\\'+'classify_data.py'
        script_url = script_url.replace('\\','/')

        identiciacion_url = os.path.abspath(r'media/identificacion/'+str(a)+'/')
        print('Url identificacion/' ,identiciacion_url)
        
        dir_SVM = os.path.abspath(r'media/banco/'+str(a)+'/models/'+str(svm_PKL))
        dir_SVM = dir_SVM.replace('\\','/')
        print('URL svm.pkl: ', dir_SVM)

        dir_codebook = os.path.abspath(r'media/banco/'+str(a)+'/models/'+str(codebook_pkl))
        dir_codebook = dir_codebook.replace('\\','/')
        print('URL codebook.pkl: ', dir_codebook)

        try:
            print('#### Inicio de clasificación#####')
            for imagen in Imagen.objects.filter(FK_proyecto = a):
                
                img = str(imagen.imagen)
                print('imagen: ',img)

                img_url = os.path.abspath(r'media/'+str(img)+'/')
                img_url = img_url.replace('\\','/')
                print('Imagen: ',img_url)

                run_script = subprocess.check_output([
                    'python', script_url,
                    input, img_url,
                    svm, str(dir_SVM),
                    codebook_file, str(dir_codebook)
                ])
                print('ejecucion del codigo')
                print('********Identificación lista************')

                identy = Etiquetados(Identificados = run_script.decode().replace("['",'').replace("']",''))
                identy.save()
                imagen.FK_identificar = identy
                imagen.save()

        except subprocess.CalledProcessError as identifier:
            print('error', identifier)

        return super().get_redirect_url(*args, **kwargs)

##--------------------Correguir aqui------------------------##
    #def get_success_url(self, args, kwargs):
        #print('Kwargs url: ',kwargs)
        #return reverse_lazy('projects:project', args=[self.object.pk]) + '?ok'

        #https://living-sun.com/es/python/703498-reverse-to-the-same-page-with-pk-as-slug-field-after-submit-errorreverse-with-no-arguments-not-found-python-django-django-views.html
##----------------------------------------------------------##        


            #https://medium.com/@a01364223/django-crea-tu-propia-galer%C3%ADa-de-im%C3%A1genes-5db6bff2828a
            #https://www.it-swarm.dev/es/python/django-como-crear-un-archivo-y-guardarlo-en-el-filefield-de-un-modelo/940188120/
            #http://blog.enriqueoriol.com/2014/07/upload-de-imagenes-con-django.html


#        https://es.stackoverflow.com/questions/261573/duda-con-updateview-en-django
 #       https://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/UpdateView/
 #       https://stackoverrun.com/es/q/2421991

 #Fernando.Gonzalez.Gonzalez.3221@outlook.es
 #00183221FreeG0nz@13z
