from django.contrib import admin
from .models import Activity, TypeOfActivity, Business, BranchStore
# Register your models here.

class BusinessAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "vat", )
    list_filter = ("title", )


class BranchStoreAdmin(admin.ModelAdmin):
    list_display = ("title", "health_regulator","region", "notify_number", "address", "address_number",)
    list_filter = ("business__title", )

admin.site.register(Business, BusinessAdmin)
admin.site.register(BranchStore, BranchStoreAdmin)
admin.site.register(Activity)
admin.site.register(TypeOfActivity)