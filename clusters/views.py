from django.shortcuts import render
from .models import Cluster
from .src import database


def cluster_list(request, url_id):

    url_id = url_id
    cluster_list = database.count_clusters(url_id)
    new_clusters = []
    for c in cluster_list:
        new_clusters.append((c[0], c[1], 'img/'+c[2], c[3]))
    cluster_list = new_clusters
    image_url = 'img/' + database.get_image_url_by_id(url_id)[0][0]
    return render(request, 'clusters.html', locals())
