from django.db import models
from django.utils.translation import gettext_lazy as _



# Create your models here.
class CommonFields(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Region(CommonFields):
    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

class RegionUnity(CommonFields):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Region Unity")
        verbose_name_plural = _("Region Unities")

class State(CommonFields):
    region_unity = models.ForeignKey(RegionUnity, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")

class ZipCode(models.Model):
    number = models.PositiveSmallIntegerField()
    slug = models.SlugField(blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)