from django.contrib import admin
from .models import Home

# Register your models here.
class HomeAdmin(admin.ModelAdmin):
    readonly_fields= ('created', 'updated')

    class Media:
        css = {
            'all': ('core/css/custom_ckeditor.css',)
        }
admin.site.register(Home, HomeAdmin)