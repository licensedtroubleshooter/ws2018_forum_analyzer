from django.shortcuts import render, redirect
from texts.src.database import get_url_with_id
from time import sleep
import src.database as db

def choice(request, url_id):
    url_id = url_id
    url = get_url_with_id(url_id)[0][0]
    return render(request, 'choice.html', locals())


def go_url(request):
    if request.method == 'POST':
        url = request.POST['url']
        # print(url)

        url_id = db.add_group_to_postgres(url)

        if url_id is None:
            return render(request, 'wait.html', locals())

        return render(request, 'choice.html', locals())

    return render(request, 'index.html', locals())
