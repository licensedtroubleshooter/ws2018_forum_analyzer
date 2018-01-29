from django.db import models


class Cluster(models.Model):

    name = models.CharField(max_length = 256)

    class Meta:
        verbose_name = "Cluster"
        verbose_name_plural = "Clusters"

    def __str__(self):
        return "{}".format(self.name)
