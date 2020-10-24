from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Activity(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    order = models.PositiveSmallIntegerField(_("Display order"), blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        # pylint: disable=too-few-public-methods
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

class TypeOfActivity(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    class Meta:
        # pylint: disable=too-few-public-methods
        verbose_name = _("Type of Activity")
        verbose_name_plural = _("Type of Activities")

class CheckListTab(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    activity = models.ManyToManyField(Activity)
    order = models.PositiveSmallIntegerField(_("Display order"), blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        # pylint: disable=too-few-public-methods
        verbose_name = _("Checklist Tab")
        verbose_name_plural = _("Checklist Tabs")


