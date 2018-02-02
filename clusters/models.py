from django.db import models


class Cluster(models.Model):

    summary = models.TextField(max_length = 10000)

    class Meta:
        verbose_name = "Cluster"
        verbose_name_plural = "Clusters"

    def __str__(self):
        return "{}".format(self.summary)
