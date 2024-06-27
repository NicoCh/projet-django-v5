from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('colloscope/<str:colloscope_id>/', views.colloscope, name='colloscope'),
    #path('results/<str:id>/', views.results, name='results'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)