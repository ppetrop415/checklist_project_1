from django.contrib import admin
from .models import CheckListTab, CheckListTabItem, Inspection, Response, Answer
# Register your models here.


class CheckListTabItemInline(admin.StackedInline):
    model = CheckListTabItem
    ordering = ("order", "tab")
    extra = 1
    prepopulated_fields = {"slug": ("title", )}

class CheckListTabInline(admin.TabularInline):
    model = CheckListTab
    extra = 0
    prepopulated_fields = {"slug": ("title", )}

class CheckListTabAdmin(admin.ModelAdmin):
    list_display = ("title", )
    list_filter = ("title", )
    prepopulated_fields = {"slug": ("title", )}

class CheckListTabItemAdmin(admin.ModelAdmin):
    list_display = ("title", "choices", "tab", )
    list_filter = ("title", )
    prepopulated_fields = {"slug": ("title", )}

class InspectionAdmin(admin.ModelAdmin):
    list_display = ("branch_store", "classification", )
    list_filter = ("classification", )
    inlines = [CheckListTabInline, CheckListTabItemInline]
    # prepopulated_fields = {"slug": ("title", )}


class ResponseAdmin(admin.ModelAdmin):
    list_display = ("inspection_uuid", "inspection", "get_inspectors", "created", )
    list_filter = ("created", )

class AnswerAdmin(admin.ModelAdmin):
    list_display = ("check_list_item", "response", "body", "created", )
    list_filter = ("created", )    


admin.site.register(CheckListTab, CheckListTabAdmin)
admin.site.register(CheckListTabItem, CheckListTabItemAdmin)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Answer, AnswerAdmin)