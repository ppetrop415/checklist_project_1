from django.contrib import admin
from .models import CheckListTab, CheckListTabItem, Choice, Inspection, Answer

# Register your models here.
class CheckListTabAdmin(admin.ModelAdmin):
    list_display = ("title", )
    list_filter = ("title", )
    prepopulated_fields = {"slug": ("title", )}

class CheckListTabItemAdmin(admin.ModelAdmin):
    list_display = ("title", "tab", "get_choices","is_important", )
    list_filter = ("title", )
    prepopulated_fields = {"slug": ("title", )}

class InspectionAdmin(admin.ModelAdmin):
    list_display = ("branch_store", "get_inspectors", "score", "classification", "uuid", "date_created", )
    list_filter = ("classification", )

class AnswerAdmin(admin.ModelAdmin):
    list_display = ("check_list_item", "body", "inspection",  "created", )
    list_filter = ("created", )    

admin.site.register(CheckListTab, CheckListTabAdmin)
admin.site.register(CheckListTabItem, CheckListTabItemAdmin)
admin.site.register(Choice)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Answer, AnswerAdmin)