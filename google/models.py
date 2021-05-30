from django.db import models
from django.db.models import JSONField


class SearchResult(models.Model):
    number_of_search = models.CharField(max_length=255)
    most_common_titles = models.TextField()
    most_common_descriptions = models.TextField()
    keyword = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()


class Link(models.Model):
    scrapper_search = models.ForeignKey(SearchResult, on_delete=models.CASCADE)
    link = models.URLField(max_length=255)


class TimeLimit(models.Model):
    time = models.IntegerField(help_text="in minutes")