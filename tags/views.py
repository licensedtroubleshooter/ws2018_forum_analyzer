from django.shortcuts import render
from .models import Tag
from .src import database


def tag_list(request, url_id):

    tag_list = database.count_tags(url_id)
    print(tag_list)
    return render(request, 'tags.html', locals())
