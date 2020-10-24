from django.db import models
from django.contrib.auth.models import User
from regions.models import Region, RegionUnity, State, ZipCode

# Create your models here.

class Business(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    VAT = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class BranchStore(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    business = models.ForeignKey(Business, on_delete=models.PROTECT)
    health_regulator = models.ForeignKey(User, on_delete=models.PROTECT)
    notify_number = models.IntegerField()
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    region_unity = models.ForeignKey(RegionUnity, on_delete=models.PROTECT)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT)
    address = models.CharField(max_length=100)
    address_number = models.PositiveSmallIntegerField()
    email = models.EmailField(max_length=150)

    def __str__(self):
        return self.title