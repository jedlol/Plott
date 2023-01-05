from django.db import models

class getLineChart(models.Model):
    PoS = models.CharField(max_length=100)
    count = models.PositiveIntegerField()