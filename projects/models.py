from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Etiqueta(models.Model):
    tag = models.CharField(verbose_name='Etiqueta', max_length = 50,)
    FK_proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE, verbose_name='FK proyecto', related_name='FKProyect')

    def __str__(self):
        return self.tag

class Proyecto(models.Model):
    FK_autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    titulo = models.CharField(verbose_name='Título', max_length=200)
    contenido = models.TextField(verbose_name='Descripción del proyecto')
    etiqueta = models.CharField(verbose_name = 'Etiqueta número uno', max_length=200, )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')

    class Meta:
        verbose_name='Proyecto'

    def __str__(self):
        return self.titulo

def repository_project_directory_path(instance, filename):
    return 'banco/%s/media/%s/%s' %(instance.FK_proyecto, instance.Etiqueta, filename)

class Repositorio(models.Model):
    FK_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name = 'FK proyecto')

    Etiqueta = models.CharField(verbose_name = 'Etiqueta', max_length=50, blank = True, null = True)

    repositorio = models.FileField(upload_to= repository_project_directory_path)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')

    class Meta:
        verbose_name='Banco de imágenes'

    def __str__(self):
        return 'Banco de: %s %s' %(self.Etiqueta, self.id)

def identification_project_directory_path(instance, filename):
    return 'identification/%s/%s' %(instance.FK_proyecto, filename)

class Imagen(models.Model):
    FK_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name = 'FK de proyecto')
    FK_identificar = models.ForeignKey('Etiquetados', on_delete=models.CASCADE, verbose_name = 'Identificados',  blank = True, null = True)
    imagen = models.ImageField(upload_to=identification_project_directory_path)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')
    
    class Meta:
        verbose_name='Identificados'

    def __str__(self):
        return 'Etiqueta: %s %s' %(self.FK_identificar, self.id)

class Etiquetados(models.Model):
    Identificados = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')

    class Meta:
        verbose_name='Etiquetados'

    def __str__(self):
        return 'Etiqueta: %s' %(self.Identificados)