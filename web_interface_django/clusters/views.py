from django.shortcuts import render
from .models import Cluster
from .src import database


def cluster_list(request):

    cluster_list = database.count_clusters()
    return render(request, 'clusters.html', locals())
