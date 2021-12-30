"""ZProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from core.urls import core_patterns
from pages.urls import urlPage
from projects.urls import urlpatterns

urlpatterns = [
    #path de Core
    path('', include(core_patterns)),
    #pah de Pages
    path('pages/', include(urlPage)),
    #path de Projects
    path('projects/', include(urlpatterns)),
    #pah de Auth
    path('accounts/',include('django.contrib.auth.urls')),
    #path de registro
    path('accounts/', include('registration.urls')),
    
    #pah de Admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)