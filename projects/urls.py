from django.urls import path, include
from .views import *

urlpatterns = ([
    path('', ProjetcsListView.as_view(), name='projects'),
    path('<int:pk>/<slug:slug>/', ProjectDetailView.as_view(), name='project'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', ProjectDeleteView.as_view(), name='delete'),
    
    path('<int:pk>/<slug:slug>/', include([
        #path de imágenes
        path('repos/',BancoImagesView.as_view(), name='repos'),
        path('image/',ImagesView.as_view(), name='image'),
        #path de algoritmos Custom Vision
        path('extract/',Extract_features_View.as_view(), name='extract'),
        path('train/',Training_View.as_view(), name='train'),
        path('identy/',clasification_View.as_view(), name='identy'),
    ]))
],'projects')