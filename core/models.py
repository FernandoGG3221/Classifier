from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Home(models.Model):
    titulo = models.CharField(max_length = 200, verbose_name= 'Título')
    description = RichTextField(verbose_name = 'Contenido')
    link = models.URLField(null=True, blank = True, verbose_name ='Link de video')
    images = models.FileField(null = True, blank = True,upload_to= 'Carrusel de inicio' , verbose_name = 'Imagenes para el carrusel')
    created = models.DateTimeField(auto_now_add= True, verbose_name= 'Creado el')
    updated = models.DateTimeField(auto_now = True, verbose_name= 'Actualizado el')

    class Meta:
        verbose_name = 'Inicio'
        verbose_name_plural = 'Sección de inicio'

    def __str__(self):
        return self.titulo