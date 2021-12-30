from django.contrib import admin
from .models import PageModel

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display = ('title','order')

    class Media:
        css = {
            'all' : ('pages/css/custom_ckeditor.css', )
        }
admin.site.register(PageModel, PageAdmin)