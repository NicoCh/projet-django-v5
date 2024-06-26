from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('colloscope/<str:colloscope_id>/', views.colloscope, name='colloscope'),

]
