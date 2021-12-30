from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    name2 = models.CharField(max_length=30,null=True, blank=True)
    name3 = models.CharField(max_length=30,null=True, blank=True)
    institute = models.CharField(max_length=60,null=True, blank=True)
    address = models.CharField(max_length=30,null=True, blank=True) 

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        ordering = ['user__username']

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    print('Instancia: ',instance)
    print('Sender: ',sender)
    print('KWargs: ',kwargs)
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        print("Se acaba de crear un usuario y su perfil enlazado")
