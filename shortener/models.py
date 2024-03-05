from django.db import models


class Urls(models.Model):
    long_url = models.CharField(max_length=1000)
    short_url = models.CharField(max_length=100)
