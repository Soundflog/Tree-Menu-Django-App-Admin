# menu/views.py
from django.shortcuts import render


def home(request):
    return render(request, '../tree_menu/templates/base.html')
