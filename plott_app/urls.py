from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='plot.html'), name='plot'),
    path('', views.button),
    path('filternal/', views.filternal),
    path('tests/', views.tests),
]