from django.contrib import admin
from .models import Region, RegionUnity, State, ZipCode
# Register your models here.


class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}

class RegionUnityAdmin(admin.ModelAdmin):
    list_display = ("title", "region",)
    list_filter = ("region", )
    prepopulated_fields = {"slug": ("title", )}

class StateAdmin(admin.ModelAdmin):
    list_display = ("title", "region_unity", )
    list_filter = ("region_unity__region", )
    prepopulated_fields = {"slug": ("title", )}

class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ("number", "state", )
    list_filter = ("state", "state__region_unity", )
    prepopulated_fields = {"slug": ("number", )}

admin.site.register(Region, RegionAdmin)
admin.site.register(RegionUnity, RegionUnityAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(ZipCode, ZipCodeAdmin)