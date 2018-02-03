from django.shortcuts import render
from .src.database import get_texts, texts_of_tag, texts_of_cluster, \
    spam_status_to_active, get_url, get_text, \
    get_cluster_summary, get_all_url
from tags.src.database import tags_of_text
from clusters.src.database import cluster_of_text


def texts_tag(request, tag, url_id):
    url_id = url_id
    tag_name = tag
    texts = get_texts(texts_of_tag(tag, url_id))
    return render(request, 'texts_tag.html', locals())


def texts_cluster(request, cluster_id, url_id):
    summary = get_cluster_summary(int(cluster_id))  #List for cluster in 'summary' (html)
    url_id = url_id
    if request.method == 'POST':
        spam = request.POST['spam']
        spam_status_to_active(int(spam))
    texts = get_texts(texts_of_cluster(int(cluster_id), url_id))
    return render(request, 'texts_cluster.html', locals())


def text_info(request, text_id, url_id):
    url_id = url_id
    text = get_text(text_id)
    cluster = cluster_of_text(text_id)
    tags = tags_of_text(text_id)
    url = get_url(text_id)
    return render(request, 'text_info.html', locals())


def urls(request):

    urls = get_all_url()
    return render(request, 'urls.html', locals())
