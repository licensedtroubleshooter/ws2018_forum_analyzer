from django.shortcuts import render
from .src.database import get_texts, texts_of_tag, texts_of_cluster


def texts_tag(request, tag):

    texts = get_texts(texts_of_tag(tag))
    return render(request, 'texts.html', locals())


def texts_cluster(request, cluster_id):

    texts = get_texts(texts_of_cluster(int(cluster_id)))
    return render(request, 'texts_clusters.html', locals())