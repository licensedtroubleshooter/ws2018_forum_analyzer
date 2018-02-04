from django.db import models


class Cluster(models.Model):

    summary = models.TextField(max_length = 10000)
    image = models.ImageField(null=True, max_length=500)

    class Meta:
        verbose_name = "Cluster"
        verbose_name_plural = "Clusters"

    def __str__(self):
        return "{}".format(self.summary)
