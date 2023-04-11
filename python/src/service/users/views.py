from django.shortcuts import render
from django.views.generic import CreateView, TemplateView

# Create your views here.


class Login(TemplateView):
    template_name='users/login.html'

