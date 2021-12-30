from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','avatar','bio','link','name','name2','name3','institute','address')

    class Media:
        css = {
            'all': ('pages/css/custom_ckeditor.css',)
        }
admin.site.register(Profile, ProfileAdmin)