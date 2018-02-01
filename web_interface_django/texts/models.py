from django.db import models
from tags.models import Tag
from clusters.models import Cluster


class Url(models.Model):

    url = models.CharField(max_length=256)

    def __str__(self):
        return "{}: {}".format(self.id, self.url)


class Text(models.Model):

    plain_text = models.TextField(null=False)
    cluster = models.ForeignKey(Cluster, blank = True, null = True)
    url = models.ForeignKey(Url, null = True, blank = True, default = None)
    status = models.SmallIntegerField(blank = False, default = 0)
    tonality = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Text"
        verbose_name_plural = "Texts"

    def __str__(self):
        return "{}. {}".format(self.id, self.plain_text)


class TagText(models.Model):

    tag = models.ForeignKey(Tag, blank = False, null = False, default = False, on_delete = models.CASCADE)
    text = models.ForeignKey(Text, blank = False, null = False, default = False, on_delete = models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.tag, self.text.plain_text)


