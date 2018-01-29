from django.db import models
from tags.models import Tag
from clusters.models import Cluster


class Text(models.Model):

    plain_text = models.TextField(null=False)
    cluster = models.ForeignKey(Cluster, blank = True, null = True, on_delete = models.CASCADE)
    source_url = models.CharField(max_length = 512, null = True, blank = True)

    class Meta:
        verbose_name = "Text"
        verbose_name_plural = "Texts"

    def __str__(self):
        return "{}. {}".format(self.id, self.plain_text)


class Tag_Text(models.Model):


    tag = models.ForeignKey(Tag, blank = False, null = False, default = False, on_delete = models.CASCADE)
    text = models.ForeignKey(Text, blank = False, null = False, default = False, on_delete = models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.tag, self.text)
