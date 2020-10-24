from django.contrib import admin
from .models import Region, RegionUnity, State, ZipCode
# Register your models here.


class RegionUnityAdmin(admin.ModelAdmin):
    list_display = ("title", "region",)
    list_filter = ("region", )

class StateAdmin(admin.ModelAdmin):
    list_display = ("title", "region_unity", )
    list_filter = ("region_unity__region", )

class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ("number", "state", )
    list_filter = ("state", "state__region_unity", )

admin.site.register(Region)
admin.site.register(RegionUnity, RegionUnityAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(ZipCode, ZipCodeAdmin)