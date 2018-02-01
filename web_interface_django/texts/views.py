from django.shortcuts import render
from .src.database import get_texts, texts_of_tag, texts_of_cluster, spam_status_to_active, get_url, get_text
from tags.src.database import tags_of_text
from clusters.src.database import cluster_of_text


def texts_tag(request, tag):

    texts = get_texts(texts_of_tag(tag))
    return render(request, 'texts_tag.html', locals())


def texts_cluster(request, cluster_id):
    if request.method == 'POST':
        spam = request.POST['spam']
        spam_status_to_active(spam)
    texts = get_texts(texts_of_cluster(int(cluster_id)))
    return render(request, 'texts_cluster.html', locals())


def text_info(request, text_id):

    text = get_text(text_id)
    cluster = cluster_of_text(text_id)
    tags = tags_of_text(text_id)
    url = get_url(text_id)
    return render(request, 'text_info.html', locals())