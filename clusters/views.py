from django.shortcuts import render
from .models import Cluster
from .src import database


def cluster_list(request, url_id):

    url_id = url_id
    cluster_list = database.count_clusters(url_id)
    return render(request, 'clusters.html', locals())
