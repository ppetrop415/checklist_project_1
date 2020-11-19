from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse 
from django.utils.translation import gettext_lazy as _

from regions.models import Region, RegionUnity, State, ZipCode, CommonFields

# Create your models here.
class Activity(CommonFields):
    order = models.PositiveSmallIntegerField(_("Display order"))
    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")
        ordering = ['order']

    def get_absolute_url(self):
        return reverse('activity-detail', kwargs={'slug': self.slug})

class TypeOfActivity(CommonFields):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
       
    class Meta:
        verbose_name = _("Type of Activity")
        verbose_name_plural = _("Type of Activities")

class Business(CommonFields):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vat = models.PositiveIntegerField()

    class Meta:
        verbose_name = _("Business")
        verbose_name_plural = _("Businessess")

class BranchStore(models.Model):

    CENTRAL = 'Central'
    BRANCH = 'Branch'
    
    DISPLAY_METHOD_CHOICES = [
        (CENTRAL, _("Central")),
        (BRANCH, _("Branch")),
    ]

    business = models.ForeignKey(Business, on_delete=models.PROTECT, related_name="branchstores")
    title = models.CharField(_("Category"), max_length=10, choices=DISPLAY_METHOD_CHOICES)
    slug = models.SlugField(blank=True)
    health_regulator = models.ForeignKey(User, on_delete=models.PROTECT)
    notify_number = models.IntegerField()
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="branchstores")
    region_unity = models.ForeignKey(RegionUnity, on_delete=models.PROTECT, related_name="branchstores")
    state = models.ForeignKey(State, on_delete=models.PROTECT, related_name="branchstores")
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, related_name="branchstores")
    address = models.CharField(max_length=100)
    address_number = models.PositiveSmallIntegerField()
    email = models.EmailField(max_length=150)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, related_name="branchstores")
    type_of_activity = models.ForeignKey(TypeOfActivity, on_delete=models.SET_NULL, null=True, related_name="branchstores")

    class Meta:
        verbose_name = _("Branh Store")
        verbose_name_plural = _("Branch Stores")

    def __str__(self):
        return str(self.notify_number)

    def get_absolute_url(self):
        return reverse('inspection-detail', kwargs={'slug': self.slug})
