from django.contrib import admin
from .models import CheckListTab, CheckListTabItem, Inspection, Response, Answer, Choise
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
    list_display = ("title", "tab", )
    list_filter = ("title", )
    prepopulated_fields = {"slug": ("title", )}

# class InspectionAdmin(admin.ModelAdmin):
#     list_display = ("branch_store", "get_inspectors", "score", "classification", )
#     list_filter = ("classification", )
#     inlines = [CheckListTabInline, CheckListTabItemInline]
#     # prepopulated_fields = {"slug": ("title", )}


# @admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    '''Admin View for Inspection'''

    list_display = ('branch_store', 'get_inspectors', 'score', 'classification', )
    list_filter = ('classification',)
    # inlines = [
    #     CheckListTabInline,
    #     CheckListTabItemInline
    # ]
    # readonly_fields = ('responses__inspection_uuid',)
    # search_fields = ('branch_store',)
    # date_hierarchy = ''
    # ordering = ('',)

class ResponseAdmin(admin.ModelAdmin):
    list_display = ("inspection_uuid", "inspection", "get_inspectors", "created", )
    list_filter = ("created", )
    readonly_fields = ('inspection_uuid', 'created',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ("check_list_item", "response", "body", "created", )
    list_filter = ("created", )    


admin.site.register(Choise)
admin.site.register(CheckListTab, CheckListTabAdmin)
admin.site.register(CheckListTabItem, CheckListTabItemAdmin)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Answer, AnswerAdmin)