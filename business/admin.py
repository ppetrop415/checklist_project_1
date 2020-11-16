from django.contrib import admin
from .models import Activity, TypeOfActivity, Business, BranchStore

# # Register your models here.
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "order", )
    list_filter = ("title", )
    prepopulated_fields = {"slug": ("title", )}

class TypeOfActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "activity", )
    list_filter = ("title", "activity",)
    prepopulated_fields = {"slug": ("title", )}

class BusinessAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "vat", )
    list_filter = ("title", )
    prepopulated_fields = {"slug": ("title", )}

class BranchStoreAdmin(admin.ModelAdmin):
    list_display = ("title", "health_regulator","region", "notify_number", "address", "address_number",)
    list_filter = ("business__title", )
    prepopulated_fields = {"slug": ("title", )}

admin.site.register(Activity, ActivityAdmin)
admin.site.register(TypeOfActivity, TypeOfActivityAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(BranchStore, BranchStoreAdmin)