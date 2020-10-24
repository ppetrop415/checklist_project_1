from django.db import models

# Create your models here.
class Region(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title

class RegionUnity(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class State(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    region_unity = models.ForeignKey(RegionUnity, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ZipCode(models.Model):
    number = models.PositiveSmallIntegerField()
    slug = models.SlugField(blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)