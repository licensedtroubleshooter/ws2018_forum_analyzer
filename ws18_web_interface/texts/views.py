from django.shortcuts import render
from .src.database import get_texts, texts_of_tag, texts_of_cluster, spam_status_to_active


def texts_tag(request, tag):

    texts = get_texts(texts_of_tag(tag))
    return render(request, 'texts_tag.html', locals())


def texts_cluster(request, cluster_id):
    if request.method == 'POST':
        spam = request.POST['spam']
        spam_status_to_active(spam)
    texts = get_texts(texts_of_cluster(int(cluster_id)))
    return render(request, 'texts_cluster.html', locals())