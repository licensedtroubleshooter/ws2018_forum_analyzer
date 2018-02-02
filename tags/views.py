from django.shortcuts import render
from .models import Tag
from .src import database


def tag_list(request):

    tag_list = database.count_tags()
    return render(request, 'tags.html', locals())
